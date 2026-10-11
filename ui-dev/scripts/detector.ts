import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

export interface HookEvent {
  hook_event_name: "PostToolUse" | "Stop";
  cwd: string;
  session_id: string;
  tool_name?: string;
  tool_input?: Record<string, unknown>;
  stop_hook_active?: boolean;
}

const require = createRequire(import.meta.url);
const cli = join(dirname(require.resolve("impeccable/package.json")), "cli", "bin", "cli.js");
// The engine prints this in its footer as the command to run. On Windows it re-quotes anything with a
// space, which would wrap `node "..."` a second time, so the .cmd shim beside this file is named instead.
const here = dirname(fileURLToPath(import.meta.url));
const self = process.platform === "win32"
  ? join(here, "impeccable.cmd")
  : `node "${join(here, "impeccable.ts")}"`;

export interface CommandResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

export function invokeImpeccable(args: string[], input: string, cwd: string): Promise<CommandResult> {
  return new Promise((resolve, reject): void => {
    const child = execFile(process.execPath, [cli, ...args], {
      cwd,
      timeout: 25_000,
      maxBuffer: 256 * 1024,
      windowsHide: true,
      env: {
        ...process.env,
        IMPECCABLE_SELF: self,
        // Skill discovery off; the engine speaks Claude's hook protocol whichever harness runs it.
        IMPECCABLE_SKILL_DIR: "",
        IMPECCABLE_PROVIDER_ID: "source",
        IMPECCABLE_HOOK_HARNESS: "claude",
        IMPECCABLE_HOOK_QUIET: "1",
      },
    }, (error, stdout, stderr): void => {
      if (error && (typeof error.code !== "number" || error.killed)) {
        reject(new Error(`ui-dev: detector process failed; check not completed. ${stderr || error.message}`, { cause: error }));
      } else {
        resolve({ stdout, stderr, exitCode: typeof error?.code === "number" ? error.code : 0 });
      }
    });
    child.stdin?.on("error", (error): void => { reject(error); });
    child.stdin?.end(input);
  });
}

export async function runDetector(event: HookEvent): Promise<string> {
  // Without these the engine fails with a bare stack trace; naming the field is the whole point.
  assert(typeof event.cwd === "string" && event.cwd.length > 0, "ui-dev: hook cwd is required");
  assert(typeof event.session_id === "string" && event.session_id.length > 0, "ui-dev: hook session_id is required");
  const { stdout, stderr, exitCode } = await invokeImpeccable(["hook"], JSON.stringify(event), event.cwd);
  if (exitCode !== 0) throw new Error(`ui-dev: hook failed; check not completed. ${stderr || stdout}`);
  if (stderr) process.stderr.write(stderr);
  if (!stdout.trim()) return "";
  const result = JSON.parse(stdout) as { hookSpecificOutput?: { additionalContext?: unknown } };
  const context = result.hookSpecificOutput?.additionalContext;
  assert(typeof context === "string", "ui-dev: unexpected detector response; check not completed");
  // The engine names its own slash commands, which do not exist here; point at what does.
  return context
    .replaceAll("/impeccable hooks", `"${self}" hooks`)
    .replaceAll("/impeccable document", "the ui-dev skill's references/design-file.md");
}

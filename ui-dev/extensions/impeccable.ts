import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { runDetector, type HookEvent } from "../scripts/detector.ts";

export default function impeccable(pi: ExtensionAPI): void {
  let dirty = false;
  let requestedFollowUp = false;
  let queue: Promise<void> = Promise.resolve();

  const scan = (event: HookEvent): Promise<string> => {
    const result = queue.then((): Promise<string> => runDetector(event));
    // The caller receives failures; recovery here only keeps the next scan runnable.
    queue = result.then((): void => {}, (): void => {});
    return result;
  };

  pi.on("session_start", async (): Promise<void> => {
    dirty = false;
    requestedFollowUp = false;
  });
  pi.on("input", async (event): Promise<void> => {
    if (event.source !== "extension") requestedFollowUp = false;
  });

  pi.on("tool_result", async (event, ctx): Promise<{ content: typeof event.content } | undefined> => {
    if (event.isError || !["write", "edit"].includes(event.toolName)) return;
    dirty = true;
    let text: string;
    try {
      text = await scan({
        hook_event_name: "PostToolUse",
        cwd: ctx.cwd,
        session_id: ctx.sessionManager.getSessionId(),
        tool_name: event.toolName === "write" ? "Write" : "Edit",
        tool_input: event.input,
      });
    } catch (error) {
      text = `ui-dev: automatic design check was not completed. ${error instanceof Error ? error.message : String(error)}`;
    }
    if (text) return { content: [...event.content, { type: "text" as const, text }] };
  });

  pi.on("agent_end", async (_event, ctx): Promise<void> => {
    if (!dirty) return;
    dirty = false;
    let text: string;
    try {
      text = await scan({
        hook_event_name: "Stop",
        cwd: ctx.cwd,
        session_id: ctx.sessionManager.getSessionId(),
      });
    } catch (error) {
      text = `ui-dev: completion design check was not completed. ${error instanceof Error ? error.message : String(error)}`;
    }
    if (!text) return;
    const triggerTurn = !requestedFollowUp;
    requestedFollowUp = true;
    pi.sendMessage({ customType: "ui-dev-detect", content: text, display: true }, {
      deliverAs: triggerTurn ? "followUp" : "nextTurn",
      triggerTurn,
    });
  });
}

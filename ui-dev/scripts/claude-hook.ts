import { runDetector, type HookEvent } from "./detector.ts";

let event: HookEvent | undefined;
try {
  let input = "";
  for await (const chunk of process.stdin) input += String(chunk);
  event = JSON.parse(input) as HookEvent;
  // A Stop that Claude is already continuing from must never block again, whatever the engine says.
  if (!(event.hook_event_name === "Stop" && event.stop_hook_active)) {
    const text = await runDetector(event);
    if (text) {
      const response = event.hook_event_name === "Stop"
        ? { decision: "block", reason: text }
        : { hookSpecificOutput: { hookEventName: "PostToolUse", additionalContext: text } };
      process.stdout.write(JSON.stringify(response));
    }
  }
} catch (error) {
  const text = `ui-dev: automatic design check was not completed. ${error instanceof Error ? error.message : String(error)}`;
  if (event?.hook_event_name === "Stop") {
    // A broken engine tells the user and lets the turn end; blocking here would loop on the fault.
    process.stdout.write(JSON.stringify({ systemMessage: text }));
  } else if (event?.hook_event_name === "PostToolUse") {
    process.stdout.write(JSON.stringify({
      hookSpecificOutput: { hookEventName: "PostToolUse", additionalContext: text },
    }));
  } else {
    console.error(text);
    process.exitCode = 1;
  }
}

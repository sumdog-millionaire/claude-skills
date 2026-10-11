import { invokeImpeccable } from "./detector.ts";

try {
  const result = await invokeImpeccable(process.argv.slice(2), "", process.cwd());
  process.stdout.write(result.stdout);
  process.stderr.write(result.stderr);
  process.exitCode = result.exitCode;
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
}

---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

TDD is the red → green loop. This skill runs that loop with **holdouts**, tests the builder never sees, and carries what makes it produce tests worth keeping: what a good test is, where tests go and the anti-patterns. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read `GLOSSARY.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs and DDRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?" Give each proposed seam a one-line note on what it catches and what it misses.

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), call the Skill tool with "codebase-design" for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing every test for the whole feature first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one slice's tests → its implementation → repeat, each slice a **tracer bullet** that responds to what the last one taught you.

## Holdouts: the builder never sees the tests

A builder that can read its tests builds to pass them, and the software ends up good only for those tests. So the tests are **holdouts**: written before the code by the `tester` agent, run by the `validator` agent, and hidden from the builder. A plugin hook blocks every other agent from the holdout folder, except its `seams.md`.

`seams.md` is the builder's contract: each seam's exact entry point, input shapes and fixtures, and nothing about what the tests check.

The agent running the build launches the tester and validator. A builder that is itself a subagent reports what it needs (a seam change, or done) to the orchestrator that launched it, which launches them instead.

## The loop

One slice at a time:

1. **Red.** Launch the `tester` agent with the ticket or spec and the slice's agreed seams. It writes the holdouts and `seams.md`, and reports only which seams it covered.
2. **Build** to `seams.md`, only enough to meet the slice. Throwaway scripts are fine for investigating; the tester's tests are the only ones committed. Keep the agreed seams. Ask the tester for a seam change only when honouring a seam would force unnatural code (contorted signatures, plumbing that exists only for the test). It changes how the tests call the code, never what they check. A change to a public interface the spec names stops the build and goes to the user.
3. **Green.** Launch the `validator` agent. It runs the holdouts and uses the app or code the way it is really used. A red report names the behaviour missed and what the code did: investigate, fix, and validate again.
4. **Way out.** After three red reports on one slice, or when the validator or builder judges a test wrong, stop and bring the evidence to the user. Tests change only with the user's agreement.

Once the build is reviewed and the user confirms it meets the intent, launch the tester to promote the holdouts into the project's tests. List any seam changes for the user at that point.

If the user opts out of holdouts, the builder writes each test itself: red before green, one seam per cycle.

**Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.

# Development context

PackWrite validated the existing `agent/` execution pack with zero warnings before
this recording. The bounded Loop cycle is capture → inspect → correct → verify.
No plugin architecture or canonical tool implementation changes are part of this film.

The first local-model launch failed Hermes's 64K minimum-context check. The
recording model was reconfigured to 65536 tokens. One later approval expired;
that invocation was blocked and a new explicitly requested invocation was required.
The film condenses these setup and operator delays; raw recordings preserve them.

A pyte 0.8.2 replay defect discarded text following emoji presentation selectors.
The renderer now removes only those presentation hints before emulation. A test
checks that the approval heading and following words survive; source casts remain
unmodified. This is a replay fix, not a change to Hermes or Kujo permissions.

Two upstream Eval Markdown lines contain trailing spaces. Their exact paths are
exempt from Git whitespace checking because changing them would invalidate the
stored artifact hashes. No generated evidence content was normalized.

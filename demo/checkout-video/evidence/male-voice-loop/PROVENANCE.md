# Loop evidence

This run used `.local/male-voice-loop/loop.yml`. The complete original iteration,
including its binary diff, remains there. This copy preserves the context, action,
gates and verdict; `diff-reference.json` records the raw patch hash and location.
The large binary patch duplicates the delivered media, so it is not copied into
the public repository. Source and media are versioned directly in Git.

To repeat, copy the config into a fresh ignored `.local/` state directory and
invoke the canonical Loop harness with that config from the repository root.

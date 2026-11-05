# Review — complete interface framing, revision 4

The user found words cut off at the left and right of the Hermes footage. Revision 3's zooms and negative offsets caused that; its review did not catch the problem. This revision removes those offsets, crops, and camera moves from all seven recording scenes, including the original CLI approval shot.

Each recording uses `object-fit: contain` inside a 1660 × 840 frame at (130, 180). The full source width remains visible throughout the scene. Only the desktop recorder's blank gray bottom padding is removed from the source clips; no horizontal pixels are discarded. The actual native interface may still truncate its own labels or collapse long messages. The edit does not create those truncations.

The targeted contact sheet covers every affected scene. The phone sheet checks the complete interface at 360 px. Full-view framing makes metadata smaller; the headline and narration retain the meaning. This tradeoff follows the user's explicit request to see the whole view. The nine glitches, original logo bumpers, narration, timing, and recorded execution evidence remain unchanged.

The full HyperFrames check passes with zero errors and no layout warnings. Ten lint warnings describe the nine explicit glitch overlays and their lane density. The sole contrast warning occurs during the outgoing glitch; stable reading frames are unaffected. `verify_edit.py` now rejects side cropping, fill stretching, and video zooms in all seven recording scenes, and verifies the preserved source width and clip hashes.

The film remains 85 seconds. Both exports receive full decoding, dimension, duration, hash, and audio-level checks. Audio is measured, not auditioned. Source and delivery evidence are under `evidence/v4-*`; final Loop gates are under `evidence/loop-v4/`. This revision browses the same saved Hermes run and makes no new model-execution or tool-certification claim.

A fresh visual reviewer found no P0/P1 issues against the full-width framing fix in all seven recording scenes. The editable preview remains available in the HyperFrames desktop app.

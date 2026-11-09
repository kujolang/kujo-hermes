"""Export optional captions from the actual generated voice alignment."""
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[1]
timeline = json.loads((root / 'timeline.json').read_text())
lines = ['WEBVTT', '']


def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    return (f'{milliseconds // 3600000:02}:{milliseconds // 60000 % 60:02}:'
            f'{milliseconds // 1000 % 60:02}.{milliseconds % 1000:03}')


for cue in timeline['cues']:
    path = root / 'evidence' / f"alignment-{cue['cue']}.json"
    if not path.exists():
        segments = [(0, cue['duration'], cue['text'])]
    else:
        alignment = json.loads(path.read_text())
        text = ''.join(alignment['characters'])
        segments = []
        for match in re.finditer(r'.{1,65}(?:\s|$)', text):
            start, end = match.span()
            segments.append((alignment['character_start_times_seconds'][start],
                             alignment['character_end_times_seconds'][end - 1],
                             match.group().strip()))
    for start, end, text in segments:
        lines.extend([f"{timestamp(cue['start'] + start)} --> "
                      f"{timestamp(cue['start'] + end)}", text, ''])
(root / 'delivery/kujo-hermes-checkout.vtt').write_text('\n'.join(lines).rstrip() + '\n')

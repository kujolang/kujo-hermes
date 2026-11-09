"""Adapt presentation selectors to pyte's text-only terminal emulator.

pyte 0.8.2 stops drawing the rest of a printable run on a non-combining
zero-width variation selector. Drop only those emoji/text presentation hints;
retain the base glyph and every following character. Raw casts remain unchanged.
"""
def replay_text(text):
    return text.replace('\ufe0e', '').replace('\ufe0f', '')

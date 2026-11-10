"""One resource boundary for source plugins and installed Python wheels."""
from pathlib import Path

_package = Path(__file__).resolve().parent
_bundled = _package / '_resources'
ROOT = _bundled if (_bundled / 'catalog/abilities.json').is_file() else _package.parent

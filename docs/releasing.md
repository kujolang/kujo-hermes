# Release packaging

Install the native plugin with Hermes, pinned to an official release:

```sh
hermes plugins install kujolang/kujo-hermes --ref 7817d3ca8b085b4582b59d13f9e6262778dcdd1c
hermes kujo setup --trust-workspace .
```

The GitHub release also includes a compact `kujo-hermes-0.1.0-plugin.zip`, a Python wheel, a source distribution and `SHA256SUMS`. The native archive omits development fixtures and video recordings. Extract its `kujo-hermes` directory into `~/.hermes/plugins`, install its Python dependencies in the Hermes environment, then run `hermes plugins doctor ~/.hermes/plugins/kujo-hermes` and enable the plugin as described in the README. The wheel supplies the Python adapter and its resources; installing it alone does not register a Hermes plugin.

Build with Python 3.11 or newer and the `build` package:

```sh
python -m build
python scripts/check-wheel.py dist/kujo_hermes-0.1.0-py3-none-any.whl
python scripts/package-release.py --output dist
python scripts/check-release.py dist/kujo-hermes-0.1.0-plugin.zip
```

Build from a clean checkout. Check the version in `pyproject.toml`, `plugin.yaml` and `kujo_hermes/__init__.py` before tagging. The archive uses fixed timestamps and sorted entries; identical inputs produce identical bytes. `check-release.py` enforces a 1 MiB native archive budget. Review intended resource growth before changing that budget. Python package artifacts retain normal setuptools build behavior; no claim of byte-for-byte wheel or sdist reproducibility is made.

Run the unit suite, both Hermes host modes, official Doctor and validation, and the checkout failure/correction fixture before publishing. CI repeats unit, package and Hermes compatibility checks. Publish only after those checks pass. Verify the uploaded asset hashes against `SHA256SUMS`.

Hermes 0.23.0 requires a full 40-character commit for `--ref`; it rejects tag names such as `v0.1.0`. The original v0.1.0 archive README predates this correction. Use the SHA above for that exact release, or omit `--ref` for the repository's current revision. Release assets and the tag remain unchanged.

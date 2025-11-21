# pyaskalono

Python bindings for [askalono](https://github.com/jpeddicord/askalono) - rust library to detect license texts

## Installation

```
pip install pyaskalono
```

## Development

To set up the development environment:

```
uv sync --all-extras
```

Then run maturin commands with:

```
uv run maturin develop
```

## Testing

The project includes a comprehensive test suite using pytest. Tests cover:
- License identification for common licenses (MIT, Apache, GPL, BSD)
- License class properties and methods
- Edge cases (empty text, unicode, partial licenses)

To run tests locally:

```bash
# Install dev dependencies (includes pytest)
uv sync --all-extras

# Build the library
uv run maturin develop

# Run tests
uv run pytest -v
```

Tests are automatically run on GitHub Actions before building wheels for any platform. All tests must pass before builds proceed.


## Use

```python
from askalono import identify

LICENSE = '''
The MIT License (MIT)

Copyright © 2021 <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

detected_license = identify(LICENSE)

detected_license.name # 'MIT'
detected_license.score # 0.9878048896789551
```

## Updating the License Cache

The `askalono-cache.bin.zstd` file contains a compressed database of license texts from [SPDX](https://github.com/spdx/license-list-data). To update it with the latest licenses:

### Using the update script (recommended)

```bash
./update_cache.sh
```

This script will:
1. Clone or update the SPDX license data repository
2. Generate a new cache file using the askalono CLI
3. Replace the existing `askalono-cache.bin.zstd`

### Manual update

If you prefer to update manually:

```bash
# Install askalono CLI if not already installed
cargo install askalono-cli

# Clone SPDX license data
git clone https://github.com/spdx/license-list-data.git

# Generate the cache file
askalono cache load-spdx --store license-list-data/json/details 

After updating the cache, rebuild the package:

```bash
uv run maturin develop
```

## Publishing

To upload new package run `uv run maturin publish`

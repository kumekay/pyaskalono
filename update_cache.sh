#!/bin/bash
set -e

echo "Updating askalono license cache..."

# Check if askalono is installed
if ! command -v askalono &> /dev/null; then
    echo "Error: askalono CLI is not installed."
    echo "Install it with: cargo install askalono-cli"
    exit 1
fi

# Clone or update SPDX license data
if [ -d "license-list-data" ]; then
    echo "Updating existing SPDX license data..."
    cd license-list-data
    git pull origin main
    cd ..
else
    echo "Cloning SPDX license data..."
    git clone https://github.com/spdx/license-list-data.git
fi

# Generate the cache file
echo "Generating cache file..."
askalono cache load-spdx --store license-list-data/json/details 

echo "Cache file updated successfully!"
echo "File size: $(du -h askalono-cache.bin.zstd | cut -f1)"
echo ""
echo "Next steps:"
echo "1. Test the new cache: uv run maturin develop"
echo "2. Verify it works: python -c 'from askalono import identify; print(identify(\"MIT License\"))'"
echo "3. Commit the updated cache file"

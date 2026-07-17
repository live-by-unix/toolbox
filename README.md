# Toolbox

A lightweight, user-friendly CLI tool for managing and running Python scripts. Toolbox makes it easy to organize, execute, and manage your personal script collection with minimal overhead.

## Overview

Toolbox provides a simple interface to:
- **Organize scripts** in a centralized location (`~/.toolbox_scripts/`)
- **Run scripts** with automatic virtual environment support
- **Manage dependencies** per-project with Toolbox's isolated venv
- **Execute system-wide** without polluting your global Python environment

The philosophy is simple: write your scripts once, organize them, and run them anywhere with one command.

## Installation

### From Source

```bash
git clone https://github.com/altforunix/tobepushed.git
cd tobepushed
pip install -e .
```

During installation, Toolbox will automatically:
1. Create `~/.toolbox/venv` (isolated virtual environment)
2. Create `~/.toolbox_scripts/` (scripts directory)
3. Initialize the environment

### From PyPI

```bash
pip install toolbox-cli
```

## Quick Start

### 1. Create a Script

Create a new Python script in `~/.toolbox_scripts/`:

```bash
cat > ~/.toolbox_scripts/hello.py << 'EOF'
#!/usr/bin/env python3
import sys

print(f"Hello, {' '.join(sys.argv[1:]) or 'World'}!")
EOF
```

### 2. Run the Script

```bash
toolbox run hello
# Output: Hello, World!

toolbox run hello Alice Bob
# Output: Hello, Alice Bob!
```

### 3. List All Scripts

```bash
toolbox list
# Output:
# Scripts in /home/user/.toolbox_scripts/:
#   - hello.py
```

## Usage

### `toolbox run <script-name> [args...]`

Execute a script from `~/.toolbox_scripts/`.

**Features:**
- Scripts run inside Toolbox's isolated virtual environment by default
- Pass arguments directly to the script
- Use `--no-venv` to run with system Python instead

**Examples:**

```bash
# Run a script with the Toolbox venv
toolbox run myscript

# Pass arguments to the script
toolbox run myscript arg1 arg2

# Run with system Python (no venv)
toolbox run myscript --no-venv

# Run with arguments and system Python
toolbox run myscript arg1 arg2 --no-venv
```

### `toolbox list`

Display all available scripts in `~/.toolbox_scripts/`.

**Example:**

```bash
toolbox list
# Output:
# Scripts in /home/user/.toolbox_scripts/:
#   - cleanup.py
#   - deploy.py
#   - hello.py
```

### `toolbox install <package-name>`

Install a Python package into Toolbox's virtual environment. The package will be available to all scripts run by Toolbox.

**Examples:**

```bash
# Install a single package
toolbox install requests

# Install a specific version
toolbox install "numpy==1.21.0"

# Install multiple packages (using pip syntax)
toolbox install "requests>=2.25.0" "click>=7.0"
```

After installation, import and use the package in your scripts:

```python
# ~/.toolbox_scripts/fetch_data.py
import requests

response = requests.get('https://api.example.com/data')
print(response.json())
```

Then run it:

```bash
toolbox run fetch_data
```

### `toolbox --version`

Print the Toolbox version.

**Example:**

```bash
toolbox --version
# Output: Toolbox 1.0.0
```

### `toolbox setup`

Manually initialize the Toolbox environment (runs automatically during installation).

**Example:**

```bash
toolbox setup
# Output:
# [Toolbox Setup] Setup complete!
# [Toolbox Setup] Virtual environment: /home/user/.toolbox/venv
# [Toolbox Setup] Scripts directory: /home/user/.toolbox_scripts
```

## Virtual Environment Support

### Default Behavior

By default, `toolbox run` executes your scripts using Toolbox's isolated virtual environment (`~/.toolbox/venv`). This ensures:
- **Dependency isolation**: Packages installed via `toolbox install` don't affect your system
- **Consistency**: Scripts run in a controlled environment
- **Safety**: Your system Python remains untouched

### Using System Python

To run a script with your system Python (bypassing the venv), use the `--no-venv` flag:

```bash
toolbox run myscript --no-venv
```

This is useful when:
- A script should use system-level packages
- You want to debug environment-specific issues
- Running scripts that need system tools

**Example:**

```bash
# Run with Toolbox venv (default)
toolbox run analyze data.csv

# Run with system Python
toolbox run analyze data.csv --no-venv
```

## Directory Structure

Toolbox uses the following directory structure:

```
~/.toolbox/                    # Toolbox home directory
├── venv/                       # Virtual environment (auto-created)
│   ├── bin/                    # Executables (python, pip, etc.)
│   ├── lib/                    # Python packages
│   └── ...

~/.toolbox_scripts/            # Your scripts directory
├── hello.py
├── cleanup.py
├── deploy.py
└── ...
```

## Examples

### Example 1: Data Processing Script

Create `~/.toolbox_scripts/process_csv.py`:

```python
#!/usr/bin/env python3
import sys
import csv

if len(sys.argv) < 2:
    print("Usage: process_csv <filename>")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```

Install pandas (if needed):

```bash
toolbox install pandas
```

Run the script:

```bash
toolbox run process_csv data.csv
```

### Example 2: Web Scraper

Create `~/.toolbox_scripts/scraper.py`:

```python
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

for title in soup.find_all('h1'):
    print(title.get_text())
```

Install dependencies:

```bash
toolbox install requests beautifulsoup4
```

Run it:

```bash
toolbox run scraper
```

### Example 3: Utility Script with Arguments

Create `~/.toolbox_scripts/backup.py`:

```python
#!/usr/bin/env python3
import sys
import shutil
from pathlib import Path
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: backup <directory>")
    sys.exit(1)

source = Path(sys.argv[1])
backup_name = f"{source.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
shutil.copytree(source, backup_name)

print(f"Backup created: {backup_name}")
```

Run it:

```bash
toolbox run backup ~/important_data
# Output: Backup created: important_data_20240101_143022
```

## Troubleshooting

### Virtual environment not found

**Problem:** `Error: Virtual environment not found at ~/.toolbox/venv`

**Solution:** Run the setup command:

```bash
toolbox setup
```

### Script not found

**Problem:** `Error: Script 'myscript.py' not found in ~/.toolbox_scripts/`

**Solution:** Make sure your script exists:

```bash
ls ~/.toolbox_scripts/
toolbox list  # Lists available scripts
```

### Package installation fails

**Problem:** `pip install` fails when installing a package

**Solution:** Ensure the virtual environment exists:

```bash
toolbox setup
toolbox install <package-name>
```

### Python import errors in scripts

**Problem:** Script can't import installed packages

**Cause:** Script is running with system Python instead of Toolbox venv

**Solution:** Ensure `--no-venv` is not used (or remove it):

```bash
# Don't use --no-venv if the package is installed in the venv
toolbox run myscript  # Good
toolbox run myscript --no-venv  # Will fail if package is venv-only
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/altforunix/tobepushed).

## License

BSD 3-Clause License - See [LICENSE](LICENSE) for details.

## Support

For issues, questions, or feature requests, please open an issue on [GitHub](https://github.com/altforunix/tobepushed/issues).

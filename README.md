# Poetry Update

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/poetry-update.svg)](https://badge.fury.io/py/poetry-update)

A command-line tool that simplifies Poetry package updates by performing safe, dependency-aware version bumps. Never worry about breaking your project's dependencies again!

## Features

- 🚀 One-command updates for single packages or entire projects
- 🔍 Smart dependency conflict detection
- ✨ Dry-run capability to preview changes
- 📝 Detailed logging for transparency
- 🔒 Maintains dependency compatibility across your project

## Installation

```bash
pip install poetry-update
```

## Usage

Update a single package:
```bash
poetry-update package-name
```

Update all packages in your project:
```bash
poetry-update --all
```

### Available Options

- `--all`, `-a`: Update all packages defined in pyproject.toml
- `--verbose`, `-v`: Enable detailed logging output
- `--dry-run`, `-d`: Preview updates without making changes
- `--help`, `-h`: Show help message and exit

## Examples

```bash
# Update a specific package
poetry-update requests

# Update all packages with verbose logging
poetry-update --all --verbose

# Preview updates without making changes
poetry-update --all --dry-run
```

## Development

Want to contribute? Great! Here's how to set up the project for development:

```bash
# Clone the repository
git clone https://github.com/rawheel/poetry-update.git
cd poetry-update

# Install dependencies
poetry install

# Run tests
poetry run pytest
```

## Why Poetry Update?

Poetry is an excellent tool for Python package management, but updating dependencies can sometimes be tricky. Poetry Update streamlines this process by:

- Automatically checking for dependency conflicts before updating
- Providing clear feedback about what will change
- Offering a safety net with dry-run capabilities
- Maintaining your project's dependency health

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

Made with ❤️ by [rawheel](https://github.com/rawheel)

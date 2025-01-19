# Poetry Update

A CLI tool to safely update Poetry packages with dependency conflict checking.

## Installation
bash
pip install poetry-update



## Usage

Update a single package:

bash
poetry-update package-name

Update all packages in your project:

bash
poetry-update --all


Options:
- `--verbose`, `-v`: Enable verbose logging
- `--all`, `-a`: Update all packages in pyproject.toml

## Features

- Safely updates Poetry packages to their latest versions
- Performs dry-run checks before actual updates
- Can update single package or all packages
- Verbose logging option for debugging
- Maintains dependency compatibility

## Development

Clone the repository:

bash
git clone https://github.com/rawheel/poetry-update.git
cd poetry-update

Install dependencies:

bash
poetry install

Run tests:

bash
poetry run pytest


## License

MIT License
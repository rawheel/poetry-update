import click
from loguru import logger
import sys
from .core import update_package, update_all_packages

@click.command()
@click.argument('package_name', required=False)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--all', '-a', 'update_all', is_flag=True, help='Update all packages')
def main(package_name: str, verbose: bool, update_all: bool):
    """
    Update Poetry package(s) to latest version safely.
    
    PACKAGE_NAME is the name of the package to update. If not provided with --all flag,
    this argument is required.
    """
    if not verbose:
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    if update_all:
        success = update_all_packages()
    elif package_name:
        success = update_package(package_name)
    else:
        logger.error("Either provide a package name or use --all flag")
        sys.exit(1)

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
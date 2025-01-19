import subprocess
import toml
from pathlib import Path
from typing import Tuple, Optional, List
from loguru import logger



def run_command(command: list) -> Tuple[str, str, int]:
    """Run a shell command and return its output"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode

def check_package_updates(package_name: str) -> Optional[str]:
    """Check if updating a package would cause any dependency conflicts"""
    # Check if poetry is installed
    stdout, stderr, code = run_command(["poetry", "--version"])
    if code != 0:
        logger.error("Poetry is not installed. Please install it first.")
        return None

    # Try to add latest version dry-run
    check_cmd = ["poetry", "add", f"{package_name}@latest", "--dry-run", "--no-interaction"]
    stdout, stderr, code = run_command(check_cmd)
    
    if code != 0:
        logger.error(f"Adding latest version of {package_name} would cause conflicts: {stderr}")
        return None
    
    return "latest"

def update_package(package_name: str) -> bool:
    """Update a single package to its latest version if safe"""
    logger.info(f"Checking updates for {package_name}...")
    
    latest_version = check_package_updates(package_name)
    if not latest_version:
        logger.error(f"Cannot safely update {package_name}")
        return False
    
    # Perform the actual update using poetry add @latest
    update_cmd = ["poetry", "add", f"{package_name}@latest", "--no-interaction"]
    stdout, stderr, code = run_command(update_cmd)
    
    if code != 0:
        logger.error(f"Failed to update {package_name}: {stderr}")
        return False
    
    logger.success(f"Successfully updated {package_name} to latest version")
    return True


def get_all_dependencies() -> List[str]:
    """Get all packages from pyproject.toml dependencies"""
    try:
        pyproject_path = Path("pyproject.toml")
        if not pyproject_path.exists():
            logger.error("pyproject.toml not found in current directory")
            raise FileNotFoundError("pyproject.toml not found in current directory")
            
        with open(pyproject_path) as f:
            pyproject = toml.load(f)
            
        # Get all dependencies excluding python itself
        dependencies = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
        return [pkg for pkg in dependencies.keys() if pkg != "python"]
        
    except Exception as e:
        logger.error(f"Error reading pyproject.toml: {e}")
        raise
    
def update_all_packages() -> bool:
    """Update all packages in pyproject.toml to their latest versions"""
    packages = get_all_dependencies()
    if not packages:
        logger.error("No packages found to update")
        return False
        
    logger.info(f"Found {len(packages)} packages to update")
    success = True
    
    for package in packages:
        if not update_package(package):
            success = False
            logger.warning(f"Failed to update {package}")
            continue
            
    return success
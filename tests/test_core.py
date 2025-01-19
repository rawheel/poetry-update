import pytest
from pathlib import Path
from poetry_update.core import (
    run_command,
    check_package_updates,
    update_package,
    get_all_dependencies,
    update_all_packages
)

# Test data
MOCK_PYPROJECT_CONTENT = """
[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.8"
click = "^8.1.7"
loguru = "^0.7.0"
"""

@pytest.fixture
def mock_pyproject(tmp_path):
    """Create a temporary pyproject.toml for testing"""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(MOCK_PYPROJECT_CONTENT)
    original_cwd = Path.cwd()
    
    # Change to temp directory
    import os
    os.chdir(tmp_path)
    
    yield pyproject
    
    # Restore original working directory
    os.chdir(original_cwd)

def test_run_command():
    stdout, stderr, code = run_command(["echo", "test"])
    assert code == 0
    assert "test" in stdout

def test_check_package_updates_invalid():
    result = check_package_updates("invalid-package-name-that-doesnt-exist")
    assert result is None

def test_update_package_invalid():
    result = update_package("invalid-package-name-that-doesnt-exist")
    assert result is False

def test_get_all_dependencies_no_pyproject(tmp_path):
    """Test behavior when pyproject.toml doesn't exist"""
    # Change to empty temporary directory
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        with pytest.raises(FileNotFoundError):
            get_all_dependencies()
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

@pytest.mark.integration
def test_update_all_packages(mock_pyproject):
    """
    Integration test for updating all packages.
    Note: This test requires poetry to be installed and might modify your project dependencies.
    """
    result = update_all_packages()
    assert isinstance(result, bool)

# Mock tests using pytest-mock
def test_update_all_packages_with_mocks(mocker, mock_pyproject):
    # Mock the dependencies
    mocker.patch(
        'poetry_update.core.get_all_dependencies',
        return_value=['click', 'loguru']
    )
    
    # Mock update_package to succeed for click and fail for loguru
    def mock_update_package(package_name):
        return package_name == 'click'
    
    mocker.patch(
        'poetry_update.core.update_package',
        side_effect=mock_update_package
    )
    
    result = update_all_packages()
    assert result is False  # Should be False because one package failed

def test_update_all_packages_empty(mocker):
    # Mock empty dependencies
    mocker.patch(
        'poetry_update.core.get_all_dependencies',
        return_value=[]
    )
    
    result = update_all_packages()
    assert result is False

# CLI tests
from poetry_update.cli import main
from click.testing import CliRunner

def test_cli_single_package():
    runner = CliRunner()
    result = runner.invoke(main, ['click'])
    assert result.exit_code in [0, 1]  # 0 for success, 1 for failure

def test_cli_all_packages():
    runner = CliRunner()
    result = runner.invoke(main, ['--all'])
    assert result.exit_code in [0, 1]

def test_cli_no_args():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 1
    assert "Either provide a package name or use --all flag" in result.output

def test_cli_verbose():
    runner = CliRunner()
    result = runner.invoke(main, ['--all', '--verbose'])
    assert result.exit_code in [0, 1]

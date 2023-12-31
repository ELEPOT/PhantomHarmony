import platform
from pathlib import Path

if platform.system() == "Windows":
    DATA_DIR = "D:/data"
elif platform.system() == "Linux":
    DATA_DIR = "/mnt/d/data"
else:
    raise f"OS Not Supported: {platform.system()}"

PROJECT_DIR = Path(__file__).parent
TEST_OUTPUT_DIR = PROJECT_DIR / "test_output"
EXAMPLE_DIR = PROJECT_DIR / "example"
DEPENDENCIES_DIR = PROJECT_DIR / "dependencies"
VENV_PYTHON_DIR = PROJECT_DIR / "venv/bin/python"
VENV_BIN_DIR = PROJECT_DIR / "venv/bin"

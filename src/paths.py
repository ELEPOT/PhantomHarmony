import platform
from pathlib import Path

import yaml

PROJECT_DIR = Path(__file__).parent.parent

CONFIG_YAML_PATH = PROJECT_DIR / "config.yaml"

with open(CONFIG_YAML_PATH, "r") as f:
    config = yaml.safe_load(f)

if platform.system() == "Windows":
    DATA_DIR = config["windows_data_dir"]
elif platform.system() == "Linux":
    DATA_DIR = config["linux_data_dir"]
else:
    raise f"OS Not Supported: {platform.system()}"

TEST_OUTPUT_DIR = PROJECT_DIR / "test_output"
EXAMPLE_DIR = PROJECT_DIR / "example"
DEPENDENCIES_DIR = PROJECT_DIR / "dependencies"
VENV_PYTHON_DIR = PROJECT_DIR / "venv/bin/python"
VENV_BIN_DIR = PROJECT_DIR / "venv/bin"

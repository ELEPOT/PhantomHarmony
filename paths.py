from pathlib import Path

import yaml
import sys

PROJECT_DIR = Path(__file__).parent

CONFIG_YAML_PATH = PROJECT_DIR / "config.yaml"

with open(CONFIG_YAML_PATH, "r") as f:
    config = yaml.safe_load(f)

DATASET_DIR = Path(config["dataset_dir"])
CACHE_DIR = Path(config["cache_dir"])
VALIDATION_DIR = Path(config["validation_dir"])
OUTPUT_DIR = Path(config["output_dir"])
NEXTCLOUD_MODEL_DIR = Path(config["nextcloud_model_dir"])

TEST_OUTPUT_DIR = PROJECT_DIR / "test_output"
EXAMPLE_DIR = PROJECT_DIR / "example"
DEPENDENCIES_DIR = PROJECT_DIR / "dependencies"
VENV_PYTHON_DIR = PROJECT_DIR / "venv/bin/python"
VENV_BIN_DIR = PROJECT_DIR / "venv/bin"
SRC_DIR = PROJECT_DIR / "src"


sys.path.append(str(SRC_DIR))

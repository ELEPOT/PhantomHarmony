import platform

if platform.system() == "Windows":
    DATA_DIR = "D:/data"
elif platform.system() == "Linux":
    DATA_DIR = "/mnt/d/data"
else:
    raise f"OS Not Supported: {platform.system()}"

import shutil
import os
import logging


def backup_file(path):
    """
    Create a backup of a file if it exists.
    Returns (success: bool, message: str)
    """
    try:
        if not os.path.exists(path):
            return False, "File does not exist."

        backup_path = path + ".bak"
        shutil.copy2(path, backup_path)

        logging.info(f"Backup created: {backup_path}")
        return True, backup_path

    except PermissionError:
        logging.exception("Permission error while creating backup.")
        return False, "Permission denied."

    except Exception as e:
        logging.exception("Unexpected error during backup.")
        return False, str(e)


def ensure_directory(path):
    """
    Ensure directory exists.
    Returns (success: bool, message: str)
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True, ""
    except Exception as e:
        logging.exception("Failed to create directory.")
        return False, str(e)
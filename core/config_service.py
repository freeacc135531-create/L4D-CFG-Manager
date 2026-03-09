import logging
from core.file_manager import backup_file, ensure_directory


class ConfigService:

    @staticmethod
    def save_config(file_path, content):
        """
        Save configuration file safely.
        Returns (success: bool, message: str)
        """
        try:
            backup_file(file_path)

            directory = file_path.rsplit("/", 1)[0]
            success, msg = ensure_directory(directory)
            if not success:
                return False, msg

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            logging.info(f"Config saved: {file_path}")
            return True, "File saved successfully."

        except Exception as e:
            logging.exception("Failed to save config.")
            return False, str(e)
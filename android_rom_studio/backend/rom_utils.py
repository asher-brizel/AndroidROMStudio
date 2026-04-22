import os
import zipfile
import shutil

class ROMUtils:
    @staticmethod
    def extract_zip(zip_path, extract_to, logger=None):
        """
        Extracts a ROM ZIP file to the specified directory.
        """
        if logger:
            logger.info(f"מחלץ קובץ ROM: {zip_path}")

        try:
            os.makedirs(extract_to, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            if logger:
                logger.info(f"חילוץ הסתיים: {extract_to}")
            return True
        except Exception as e:
            if logger:
                logger.error(f"שגיאה בחילוץ: {str(e)}")
            return False

    @staticmethod
    def scan_for_apks(directory, logger=None):
        """
        Scans a directory recursively and returns a list of APK paths.
        """
        if logger:
            logger.info(f"סורק קבצי APK ב: {directory}")

        apk_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.apk'):
                    apk_files.append(os.path.join(root, file))

        if logger:
            logger.info(f"נמצאו {len(apk_files)} קבצי APK.")
        return apk_files

    @staticmethod
    def check_critical_files(directory, logger=None):
        """
        Validates the structure of the extracted ROM by checking for critical files/folders.
        Does not attempt emulation.
        """
        critical_items = [
            "META-INF/com/google/android/updater-script",
            "system",
            "boot.img"
        ]

        all_found = True
        missing_items = []

        for item in critical_items:
            item_path = os.path.join(directory, item)
            # Check if item exists (either file or directory)
            if not os.path.exists(item_path):
                all_found = False
                missing_items.append(item)

        if logger:
            if all_found:
                logger.info("בדיקת ROM תקינה: כל קבצי הליבה נמצאו.")
            else:
                logger.warning(f"אזהרה: חסרים קבצי ליבה ב-ROM: {', '.join(missing_items)}")

        return all_found

    @staticmethod
    def repack_zip(source_dir, output_zip, logger=None):
        """
        Repacks a directory into a ZIP file.
        """
        if logger:
            logger.info(f"אורז מחדש ROM ל: {output_zip}")

        try:
            # Ensure the directory containing the output file exists
            os.makedirs(os.path.dirname(os.path.abspath(output_zip)), exist_ok=True)

            with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Archive path relative to source_dir
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)

            if logger:
                logger.info(f"אריזה הסתיימה בהצלחה.")
            return True
        except Exception as e:
            if logger:
                logger.error(f"שגיאה באריזה מחדש: {str(e)}")
            return False

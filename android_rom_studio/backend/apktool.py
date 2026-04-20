import subprocess
import os

class ApktoolWrapper:
    @staticmethod
    def decompile_apk(apk_path, output_dir, logger=None):
        """
        Decompile APK using apktool.
        Assumes 'apktool' is installed and available in PATH.
        """
        if logger:
            logger.info(f"מפענח APK: {apk_path}")

        try:
            # -f forces overwrite, -o specifies output directory
            result = subprocess.run(
                ["apktool", "d", "-f", apk_path, "-o", output_dir],
                capture_output=True, text=True, check=True
            )
            if logger:
                logger.info(f"פענוח הסתיים בהצלחה: {output_dir}")
            return True
        except subprocess.CalledProcessError as e:
            if logger:
                logger.error(f"שגיאה בפענוח APK: {e.stderr}")
            return False
        except FileNotFoundError:
            if logger:
                logger.error("apktool לא נמצא. אנא ודא שהוא מותקן.")
            return False

    @staticmethod
    def recompile_apk(source_dir, output_apk, logger=None):
        """
        Recompile APK using apktool.
        """
        if logger:
            logger.info(f"בונה מחדש APK מ: {source_dir}")

        try:
            result = subprocess.run(
                ["apktool", "b", source_dir, "-o", output_apk],
                capture_output=True, text=True, check=True
            )
            if logger:
                logger.info(f"בנייה הסתיימה בהצלחה: {output_apk}")
            return True
        except subprocess.CalledProcessError as e:
            if logger:
                logger.error(f"שגיאה בבניית APK: {e.stderr}")
            return False
        except FileNotFoundError:
            if logger:
                logger.error("apktool לא נמצא. אנא ודא שהוא מותקן.")
            return False

    @staticmethod
    def sign_apk(apk_path, logger=None):
        """
        Placeholder for APK signing.
        In a real scenario, this would use apksigner or jarsigner with a keystore.
        """
        if logger:
            logger.info(f"חותם על APK (מדומה): {apk_path}")

        # Placeholder success
        return True

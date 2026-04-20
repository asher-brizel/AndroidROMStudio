import os
import tempfile
import shutil
from backend.rom_utils import ROMUtils
from backend.plugins import (
    GoogleAppsRemoverPlugin,
    StatusBarIconHiderPlugin,
    SettingsCleanerPlugin
)

class ROMPipeline:
    def __init__(self, logger):
        self.logger = logger
        self.work_dir = None
        self.extracted_dir = None

        # Available plugins map
        self.plugins = {
            'removeGapps': GoogleAppsRemoverPlugin(),
            'hideStatusIcons': StatusBarIconHiderPlugin(),
            'editSettings': SettingsCleanerPlugin(),
            # Add more as needed
        }

    def extract_rom(self, zip_path):
        """Step 1: Extract ROM"""
        self.logger.info(f"מתחיל חילוץ ROM: {zip_path}")
        self.work_dir = tempfile.mkdtemp(prefix="rom_studio_")
        self.extracted_dir = os.path.join(self.work_dir, "extracted")

        success = ROMUtils.extract_zip(zip_path, self.extracted_dir, self.logger)
        return success

    def analyze_system_apps(self):
        """Step 2: Analyze system apps and structure"""
        self.logger.info("מנתח מבנה מערכת וקובצי APK...")

        if not self.extracted_dir:
            self.logger.error("אין ROM מחולץ לניתוח.")
            return False

        system_dir = os.path.join(self.extracted_dir, "system")
        if os.path.exists(system_dir):
            apk_files = ROMUtils.scan_for_apks(system_dir, self.logger)
            self.logger.info(f"ניתוח הושלם. נמצאו {len(apk_files)} אפליקציות מערכת.")
            return True
        else:
            self.logger.warning("לא נמצאה תיקיית system. ה-ROM עשוי להיות במבנה שונה (למשל payload.bin).")
            # For simplicity, we assume traditional ZIP structure here, but note the warning
            return True

    def apply_user_selected_patches(self, options):
        """Step 3: Apply selected plugins"""
        self.logger.info("מחיל עדכונים ושינויים מבוקשים...")

        context = {
            'extracted_dir': self.extracted_dir,
            'logger': self.logger
        }

        for option_key, is_selected in options.items():
            if is_selected and option_key in self.plugins:
                plugin = self.plugins[option_key]
                self.logger.info(f"מפעיל פלאגין מותאם: {plugin.name()}")
                success = plugin.apply(context)
                if not success:
                    self.logger.error(f"הפעלת פלאגין {plugin.name()} נכשלה.")
                    return False

        self.logger.info("כל השינויים הוחלו בהצלחה.")
        return True

    def rebuild_rom(self, original_zip_path):
        """Step 4: Rebuild the ROM"""
        self.logger.info("בונה מחדש את קובץ ה-ROM...")

        # Determine output path
        dir_name = os.path.dirname(original_zip_path)
        base_name = os.path.basename(original_zip_path)
        name, ext = os.path.splitext(base_name)
        output_zip = os.path.join(dir_name, f"{name}_modded{ext}")

        success = ROMUtils.repack_zip(self.extracted_dir, output_zip, self.logger)

        if success:
            self.logger.info(f"ROM מוכן: {output_zip}")
            self.cleanup()
        return success

    def cleanup(self):
        """Clean up temporary files."""
        if self.work_dir and os.path.exists(self.work_dir):
            self.logger.info("מנקה קבצים זמניים...")
            shutil.rmtree(self.work_dir)
            self.work_dir = None
            self.extracted_dir = None

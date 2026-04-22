import os
import sys
import webview
import threading
from backend.pipeline import ROMPipeline
from backend.rom_utils import ROMUtils

def get_base_path():
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# Ensure we can import from backend
sys.path.append(get_base_path())

class UILogger:
    def __init__(self, window):
        self.window = window

    def _log(self, message, level):
        # Escape quotes for JS
        safe_message = message.replace("'", "\\'").replace('"', '\\"')
        try:
            self.window.evaluate_js(f"logMessage('{safe_message}', '{level}')")
        except Exception as e:
            print(f"Log Error: {e} - Original Message: {message}")

    def info(self, message):
        print(f"[INFO] {message}")
        self._log(message, 'info')

    def warning(self, message):
        print(f"[WARN] {message}")
        self._log(message, 'warning')

    def error(self, message):
        print(f"[ERROR] {message}")
        self._log(message, 'error')


class ROMStudioAPI:
    def __init__(self):
        self.window = None
        self.logger = None

    def set_window(self, window):
        self.window = window
        self.logger = UILogger(window)

    def select_rom_file(self):
        """Opens a file dialog to select a ZIP file."""
        if not self.window:
            return None

        file_types = ('ROM ZIP Files (*.zip)', 'All files (*.*)')
        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=False,
            file_types=file_types
        )

        if result and len(result) > 0:
            return result[0]
        return None

    def _process_rom_thread(self, rom_path, options):
        try:
            self.logger.info(f"התחלת תהליך עיבוד עבור: {rom_path}")

            pipeline = ROMPipeline(self.logger)

            # Step 1
            if not pipeline.extract_rom(rom_path):
                self.logger.error("תהליך בוטל עקב שגיאה בחילוץ.")
                return

            # Step 2
            if not pipeline.analyze_system_apps():
                self.logger.error("תהליך בוטל עקב שגיאה בניתוח.")
                return

            # Step 3
            if not pipeline.apply_user_selected_patches(options):
                self.logger.error("תהליך בוטל עקב שגיאה בהחלת שינויים.")
                return

            # Step 4
            if not pipeline.rebuild_rom(rom_path):
                self.logger.error("תהליך בוטל עקב שגיאה בבנייה מחדש.")
                return

            self.logger.info("=========================================")
            self.logger.info("עיבוד ROM הסתיים בהצלחה!")
            self.logger.info("=========================================")

        except Exception as e:
            if self.logger:
                self.logger.error(f"שגיאה בלתי צפויה: {str(e)}")
            else:
                print(f"Critical error: {e}")

    def process_rom(self, rom_path, options):
        """Starts the ROM processing pipeline in a separate thread."""
        if not self.logger:
            return

        thread = threading.Thread(
            target=self._process_rom_thread,
            args=(rom_path, options)
        )
        thread.daemon = True
        thread.start()

    def _check_rom_thread(self, rom_path):
        try:
            self.logger.info(f"מתחיל בדיקת מבנה ROM עבור: {rom_path}")

            # Create a temporary directory for partial extraction to check
            import tempfile
            import shutil
            import zipfile

            temp_dir = tempfile.mkdtemp(prefix="rom_check_")

            try:
                # We don't need to extract everything, just check contents
                self.logger.info("בודק תוכן קובץ ZIP...")
                with zipfile.ZipFile(rom_path, 'r') as zip_ref:
                    file_list = zip_ref.namelist()

                # Check for critical items in the namelist
                critical_items = [
                    "META-INF/com/google/android/updater-script",
                    "system/",
                    "boot.img"
                ]

                all_found = True
                missing_items = []

                for item in critical_items:
                    # Check if any file in the zip starts with the item name (for directories)
                    if not any(f.startswith(item) for f in file_list):
                        all_found = False
                        missing_items.append(item)

                if all_found:
                    self.logger.info("בדיקת ROM תקינה: כל קבצי הליבה נמצאו במבנה ה-ZIP.")
                else:
                    self.logger.warning(f"אזהרה: חסרים קבצי ליבה ב-ROM: {', '.join(missing_items)}")

            finally:
                shutil.rmtree(temp_dir)

        except Exception as e:
            if self.logger:
                self.logger.error(f"שגיאה במהלך בדיקת ROM: {str(e)}")

    def check_rom(self, rom_path):
        """Starts the ROM check process in a separate thread."""
        if not self.logger:
            return

        thread = threading.Thread(
            target=self._check_rom_thread,
            args=(rom_path,)
        )
        thread.daemon = True
        thread.start()

def main():
    api = ROMStudioAPI()

    # Path to the UI files
    ui_path = os.path.join(get_base_path(), 'ui', 'index.html')

    window = webview.create_window(
        'Android ROM Studio',
        url=f'file://{ui_path}',
        js_api=api,
        width=900,
        height=700,
        text_select=True
    )

    api.set_window(window)
    webview.start(debug=True)

if __name__ == '__main__':
    main()

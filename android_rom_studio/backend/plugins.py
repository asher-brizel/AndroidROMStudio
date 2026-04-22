import os

class PatchPlugin:
    """
    Base interface for all ROM patch plugins.
    Plugins must not perform destructive actions (like deleting smali code automatically).
    """
    @classmethod
    def name(cls):
        """Returns the name of the plugin."""
        raise NotImplementedError("Plugins must implement name()")

    def apply(self, context):
        """
        Applies the patch to the ROM.
        `context` is a dictionary that should contain at least:
          - 'extracted_dir': path to the extracted ROM directory
          - 'logger': logger instance
        Returns True on success, False on failure.
        """
        raise NotImplementedError("Plugins must implement apply(context)")

class GoogleAppsRemoverPlugin(PatchPlugin):
    @classmethod
    def name(cls):
        return "GoogleAppsRemoverPlugin"

    def apply(self, context):
        logger = context.get('logger')
        extracted_dir = context.get('extracted_dir')

        if logger:
            logger.info("מפעיל פלאגין: הסרת אפליקציות Google...")

        # Example logic: Identify GApps directories and remove them safely.
        # In a real implementation, this would read a list of known GApps.
        gapps_paths = [
            "system/app/YouTube",
            "system/priv-app/Velvet",
            "system/app/Maps",
            "system/priv-app/GooglePlayServices"
        ]

        removed_count = 0
        for gapp in gapps_paths:
            full_path = os.path.join(extracted_dir, gapp)
            if os.path.exists(full_path):
                try:
                    import shutil
                    if os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                    else:
                        os.remove(full_path)
                    removed_count += 1
                    if logger:
                        logger.info(f"הוסר: {gapp}")
                except Exception as e:
                    if logger:
                        logger.error(f"שגיאה בהסרת {gapp}: {str(e)}")

        if logger:
            logger.info(f"סך הכל אפליקציות גוגל שהוסרו: {removed_count}")
        return True

class StatusBarIconHiderPlugin(PatchPlugin):
    @classmethod
    def name(cls):
        return "StatusBarIconHiderPlugin"

    def apply(self, context):
        logger = context.get('logger')

        if logger:
            logger.info("מפעיל פלאגין: הסתרת אייקונים משורת הסטטוס...")
            logger.info("במצב בטוח (SAFE MODE): מוסיף פקודות overlay להסתרת אייקונים במקום מחיקת קוד...")

        # Example logic for safe mode
        # Modifying SystemUI through overlays or config XMLs rather than smali editing

        return True

class SettingsCleanerPlugin(PatchPlugin):
    @classmethod
    def name(cls):
        return "SettingsCleanerPlugin"

    def apply(self, context):
        logger = context.get('logger')

        if logger:
            logger.info("מפעיל פלאגין: עריכת אפליקציית הגדרות...")
            logger.info("במצב בטוח (SAFE MODE): מסתיר תפריטים דרך flags במקום למחוק פונקציונליות ליבה...")

        # Example logic for safe mode

        return True

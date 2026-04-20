# PyInstaller build script for Android ROM Studio
import os
import subprocess
import sys

def build():
    print("Building Android ROM Studio with PyInstaller...")

    add_data_arg = "--add-data=android_rom_studio/ui:ui"
    if sys.platform.startswith('win'):
        add_data_arg = "--add-data=android_rom_studio/ui;ui"

    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "AndroidROMStudio",
        "--hidden-import", "webview",
        "--hidden-import", "backend.pipeline",
        "--hidden-import", "backend.rom_utils",
        "--hidden-import", "backend.plugins",
        "--hidden-import", "backend.apktool",
        "--hidden-import", "PyQt6",
        "--exclude-module", "PyQt5",
        "--exclude-module", "PySide2",
        "--exclude-module", "PySide6",
        "--exclude-module", "gi",
        add_data_arg,
        "android_rom_studio/main.py"
    ]

    try:
        subprocess.run(cmd, check=True)
        print("Build completed successfully! Check the 'dist' folder.")
    except Exception as e:
        print(f"Build failed: {e}")

if __name__ == "__main__":
    build()

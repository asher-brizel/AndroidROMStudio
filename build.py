# PyInstaller build script for Android ROM Studio
import os
import subprocess
import sys
import site

def build():
    print("Installing/Verifying requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to install requirements: {e}")

    print("Building Android ROM Studio with PyInstaller...")

    add_data_arg = "--add-data=android_rom_studio/ui:ui"
    if sys.platform.startswith('win'):
        add_data_arg = "--add-data=android_rom_studio/ui;ui"

    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--clean",
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
        "--collect-all", "webview",
        "--copy-metadata", "pywebview",
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

// Expose functions to pywebview
function logMessage(message, level = 'info') {
    const consoleOutput = document.getElementById('consoleOutput');
    const entry = document.createElement('div');
    entry.className = `log-entry log-${level}`;

    // Add timestamp
    const now = new Date();
    const timeString = now.toLocaleTimeString();

    entry.textContent = `[${timeString}] ${message}`;
    consoleOutput.appendChild(entry);

    // Auto-scroll to bottom
    consoleOutput.scrollTop = consoleOutput.scrollHeight;
}

async function browseFile() {
    if (window.pywebview) {
        try {
            const filepath = await window.pywebview.api.select_rom_file();
            if (filepath) {
                document.getElementById('romPath').value = filepath;
                logMessage(`נבחר קובץ: ${filepath}`);
            }
        } catch (error) {
            logMessage(`שגיאה בבחירת קובץ: ${error}`, 'error');
        }
    } else {
        logMessage('ממשק פייתון לא זמין', 'error');
    }
}

function getSelectedOptions() {
    return {
        removeGapps: document.getElementById('removeGapps').checked,
        hideStatusIcons: document.getElementById('hideStatusIcons').checked,
        editSystemUI: document.getElementById('editSystemUI').checked,
        editSettings: document.getElementById('editSettings').checked,
        removeSystemApps: document.getElementById('removeSystemApps').checked
    };
}

async function processROM() {
    const romPath = document.getElementById('romPath').value;
    if (!romPath) {
        logMessage('אנא בחר קובץ ROM תחילה', 'warning');
        return;
    }

    const options = getSelectedOptions();

    if (window.pywebview) {
        logMessage('מתחיל עיבוד ROM...', 'info');
        try {
            await window.pywebview.api.process_rom(romPath, options);
        } catch (error) {
            logMessage(`שגיאת עיבוד: ${error}`, 'error');
        }
    } else {
        logMessage('ממשק פייתון לא זמין', 'error');
    }
}

async function checkROM() {
    const romPath = document.getElementById('romPath').value;
    if (!romPath) {
        logMessage('אנא בחר קובץ ROM תחילה', 'warning');
        return;
    }

    if (window.pywebview) {
        logMessage('מתחיל בדיקת ROM...', 'info');
        try {
            await window.pywebview.api.check_rom(romPath);
        } catch (error) {
            logMessage(`שגיאת בדיקה: ${error}`, 'error');
        }
    } else {
        logMessage('ממשק פייתון לא זמין', 'error');
    }
}

// Initial connection test
window.addEventListener('pywebviewready', function() {
    logMessage('מערכת מוכנה - מחובר למנוע פייתון', 'info');
});
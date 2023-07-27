const exportUrl = document.getElementById('exportButton').getAttribute('data-export-url');
const syncUrl = document.getElementById('syncButton').getAttribute('data-sync-url');

let syncIntervalId = null;
let syncActive = false;

function toggleButtonStates(syncActive) {
    const exportButton = document.getElementById('exportButton');
    const syncButton = document.getElementById('syncButton');
    const stopSyncButton = document.getElementById('stopSyncButton');
    if (syncActive) {
        exportButton.disabled = true;
        syncButton.disabled = true;
        stopSyncButton.disabled = false;
    } else {
        exportButton.disabled = false;
        syncButton.disabled = false;
        stopSyncButton.disabled = true;
    }
}

function toggleButtonColors(syncActive) {
    const exportButton = document.getElementById('exportButton');
    const syncButton = document.getElementById('syncButton');
    const stopSyncButton = document.getElementById('stopSyncButton');

    if (syncActive) {
        syncButton.classList.remove('start-active');
        syncButton.classList.add('inactive');

        stopSyncButton.classList.remove('inactive')
        stopSyncButton.classList.add('stop-active')

        exportButton.classList.remove('start-active')
        exportButton.classList.add('inactive')
    } else {
        syncButton.classList.remove('inactive');
        syncButton.classList.add('start-active');

        stopSyncButton.classList.remove('stop-active')
        stopSyncButton.classList.add('inactive')

        exportButton.classList.remove('inactive')
        exportButton.classList.add('start-active')
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const exportButton = document.getElementById('exportButton');
    const syncButton = document.getElementById('syncButton');
    const stopSyncButton = document.getElementById('stopSyncButton');

    toggleButtonStates(syncActive);
    toggleButtonColors(syncActive);

    exportButton.addEventListener('click', () => {
        const botToken = document.getElementById('bot_token').value;
        const chatId = document.getElementById('calls_chat_id').value;
        exportCallsToTelegram(botToken, chatId);
    });

    syncButton.addEventListener('click', () => {
        const botToken = document.getElementById('bot_token').value;
        const chatId = document.getElementById('calls_chat_id').value;
        keepCallInfoSynced(botToken, chatId);

        syncActive = true;
        toggleButtonColors(syncActive);
        toggleButtonStates(syncActive);
        console.log("Button states changed due to synchronization start.")
    });

    stopSyncButton.addEventListener('click', () => {
        stopCallInfoSync();

        syncActive = false;
        toggleButtonColors(syncActive);
        toggleButtonStates(syncActive);
        console.log("Button states changed due to synchronization interruption.")
    });


});

function exportCallsToTelegram(botToken, chatId) {
    fetch(exportUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            'bot_token': botToken,
            'calls_chat_id': chatId
        })
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });
}

function keepCallInfoSynced(botToken, chatId) {
    syncIntervalId = setInterval(() => {
        fetch(syncUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams({
                'bot_token': botToken,
                'calls_chat_id': chatId
            })
        })
        .then(response => response.text())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
    }, 10000);
    console.log("Continuous synchronization started.")
}

function stopCallInfoSync() {
    clearInterval(syncIntervalId);
    console.log("Continuous synchronization interrupted.");
}


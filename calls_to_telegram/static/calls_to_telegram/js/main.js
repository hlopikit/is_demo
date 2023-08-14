import { exportCalls, initiateSyncLoop, getCurrentFlagState, setFlagState } from './bitrix_integration.js';

const exportButton = document.getElementById('exportButton');
const syncButton = document.getElementById('syncButton');
const stopSyncButton = document.getElementById('stopSyncButton');

const urls = JSON.parse(document.getElementById('app-urls').textContent);

let currentFlagState = undefined;

document.addEventListener('DOMContentLoaded', () => {
    exportButton.disabled = true;
    syncButton.disabled = true;
    stopSyncButton.disabled = true;
    getCurrentFlagState(urls.getFlagUrl)
        .then(response => {
            toggleButtonStates(response);
            toggleButtonColors(response);
            currentFlagState = response
        });

    exportButton.addEventListener('click', () => {
        exportButton.disabled = true;
        exportButton.classList.remove('start-active');
        exportButton.classList.add('inactive');
        exportCalls(urls.exportCallsUrl)
            .then(result => {
                console.log(result);
                exportButton.disabled = false;
                exportButton.classList.remove('inactive');
                exportButton.classList.add('start-active');
            })
    });

    syncButton.addEventListener('click', () => {
        currentFlagState = true;
        toggleButtonStates(currentFlagState);
        toggleButtonColors(currentFlagState);
        setFlagState(urls.setFlagUrl, currentFlagState)
            .then(() => {
                console.log("Flag set to true.");
                initiateSyncLoop(urls.keepSyncedUrl)
            })
            .catch(error => console.error("Flag setting failed.", error));
    });

    stopSyncButton.addEventListener('click', () => {
        currentFlagState = false;
        toggleButtonColors(currentFlagState);
        toggleButtonStates(currentFlagState);

        setFlagState(urls.setFlagUrl, currentFlagState)
            .then(() => console.log("Flag set to false."))
            .catch(error => console.error("Flag setting failed.", error));
    });
});

function toggleButtonStates(currentFlagState) {
    console.log(currentFlagState)
    if (currentFlagState === true) {
        exportButton.disabled = true;
        syncButton.disabled = true;
        stopSyncButton.disabled = false;

    } else {
        exportButton.disabled = false;
        syncButton.disabled = false;
        stopSyncButton.disabled = true;
    }
}

function toggleButtonColors(currentFlagState) {
    if (currentFlagState === true) {
        syncButton.classList.remove('start-active');
        syncButton.classList.add('inactive');

        stopSyncButton.classList.remove('inactive');
        stopSyncButton.classList.add('stop-active');

        exportButton.classList.remove('start-active');
        exportButton.classList.add('inactive')

    } else {
        syncButton.classList.remove('inactive');
        syncButton.classList.add('start-active');

        stopSyncButton.classList.remove('stop-active');
        stopSyncButton.classList.add('inactive');

        exportButton.classList.remove('inactive');
        exportButton.classList.add('start-active');
    }
}

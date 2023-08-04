import {finishTasks, setFlagState, getCurrentFlagState, initiateAutoFinishLoop} from './bitrix_integration.js';

const finishButton = document.getElementById('finishButton');
const syncButton = document.getElementById('syncButton');
const stopSyncButton = document.getElementById('stopSyncButton');

const urls = JSON.parse(document.getElementById('app-urls').textContent);
let currentFlagState = undefined;


document.addEventListener('DOMContentLoaded', () => {
    finishButton.disabled = true;
    syncButton.disabled = true;
    stopSyncButton.disabled = true;
    getCurrentFlagState(urls.getFlagUrl)
        .then(response => {
            toggleButtonStates(response);
            toggleButtonColors(response);
            currentFlagState = response
        });

    finishButton.addEventListener('click', () => {
        finishButton.disabled = true;
        finishButton.classList.remove('start-active');
        finishButton.classList.add('inactive');
        finishTasks(urls.finishTasksUrl)
            .then(() => {
                finishButton.disabled = false;
                finishButton.classList.remove('inactive');
                finishButton.classList.add('start-active');
            })
    });

    syncButton.addEventListener('click', () => {
        currentFlagState = true;
        toggleButtonStates(currentFlagState);
        toggleButtonColors(currentFlagState);
        setFlagState(urls.setFlagUrl, currentFlagState)
            .then(() => {
                console.log("Flag set to true.");
                initiateAutoFinishLoop(urls.initiateLoopUrl)
                    .then(() => console.log("Synchronization started successfully"))
                    .catch(error => {
                        console.error("Activity autocompletion start failed.")
                    })

            })
            .catch(error => {
                console.error("Flag setting failed.", error)
            });
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
        finishButton.disabled = true;
        syncButton.disabled = true;
        stopSyncButton.disabled = false;

    } else {
        finishButton.disabled = false;
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

        finishButton.classList.remove('start-active');
        finishButton.classList.add('inactive')

    } else {
        syncButton.classList.remove('inactive');
        syncButton.classList.add('start-active');

        stopSyncButton.classList.remove('stop-active');
        stopSyncButton.classList.add('inactive');

        finishButton.classList.remove('inactive');
        finishButton.classList.add('start-active');
    }
}



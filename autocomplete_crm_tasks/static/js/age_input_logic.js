const completeButton = document.getElementById('completeButton');
const syncButton = document.getElementById('syncButton');
const stopSyncButton = document.getElementById('stopSyncButton');

const completeTasksUrl = document.getElementById('completeButton').getAttribute('complete-tasks-url');
const setFlagUrl = document.getElementById('syncButton').getAttribute('set-flag-url')

let syncActive = false;

function completeTasks() {
    return new Promise((resolve, reject) => {
        let checkboxValues = Array.from(document.querySelectorAll('input[name="activity_type"]'))
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);
        let intervalUnit = document.getElementById('interval_unit').value;
        let intervalValue = document.getElementById('interval_value').value;
        console.log(checkboxValues);
        fetch(completeTasksUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams({
                'activity_type': checkboxValues,
                'interval_unit': intervalUnit,
                'interval_value': intervalValue,
            })
        })
            .then(() => resolve())
            .catch(error => {
                console.error(error);
                reject(error);
            });
    });
}



function setFlag(syncActive) {
    return new Promise((resolve, reject) => {
        fetch(setFlagUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams({
                'state': syncActive
            })
        })
        .then(() => resolve())
        .catch(error => {
            console.error(error);
            reject(error);
        });
    });
}


function updateIntervalOptions() {
    let intervalNumber = parseInt(document.getElementById('interval_value').value);
    let intervalUnitSelect = document.getElementById('interval_unit');
    let intervalUnitOptions = intervalUnitSelect.getElementsByTagName('option');

    for (let i = 0; i < intervalUnitOptions.length; i++) {
        let intervalUnit = intervalUnitOptions[i].value;
        let intervalUnitRussian = '';

        if (intervalNumber % 10 === 1 && intervalNumber % 100 !== 11) {
            intervalUnitRussian = {
                'minutes': 'минута',
                'hours': 'час',
                'days': 'день',
                'weeks': 'неделя',
                'years': 'год',
            }[intervalUnit];
        } else if (intervalNumber % 10 >= 2 && intervalNumber % 10 <= 4 && (intervalNumber % 100 < 10 || intervalNumber % 100 >= 20)) {
            intervalUnitRussian = {
                'minutes': 'минуты',
                'hours': 'часа',
                'days': 'дня',
                'weeks': 'недели',
                'years': 'года',
            }[intervalUnit];
        } else {
            intervalUnitRussian = {
                'minutes': 'минут',
                'hours': 'часов',
                'days': 'дней',
                'weeks': 'недель',
                'years': 'лет',
            }[intervalUnit];
        }

        intervalUnitOptions[i].textContent = intervalUnitRussian;
    }
}

function toggleButtonStates(syncActive) {
    if (syncActive) {
        completeButton.disabled = true;
        syncButton.disabled = true;
        stopSyncButton.disabled = false;
    } else {
        completeButton.disabled = false;
        syncButton.disabled = false;
        stopSyncButton.disabled = true;
    }
}

function toggleButtonColors(syncActive) {
    if (syncActive) {
        syncButton.classList.remove('start-active');
        syncButton.classList.add('inactive');

        stopSyncButton.classList.remove('inactive');
        stopSyncButton.classList.add('stop-active');

        completeButton.classList.remove('start-active');
        completeButton.classList.add('inactive')
    } else {
        syncButton.classList.remove('inactive');
        syncButton.classList.add('start-active');

        stopSyncButton.classList.remove('stop-active');
        stopSyncButton.classList.add('inactive');

        completeButton.classList.remove('inactive');
        completeButton.classList.add('start-active');
    }
}

document.addEventListener('DOMContentLoaded', () => {

    toggleButtonStates(syncActive);
    toggleButtonColors(syncActive);

    completeButton.addEventListener('click', () => {
        completeTasks()
            .then(() => console.log("Activities finished successfully."))
            .catch((error => console.error("Task finishing error.", error)));
    });

    syncButton.addEventListener('click', () => {
        syncActive = true;
        toggleButtonColors(syncActive);
        toggleButtonStates(syncActive);

        setFlag(syncActive)
            .then(() => {
                console.log("Flag set to true.");
                completeTasks()
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
        syncActive = false;
        toggleButtonColors(syncActive);
        toggleButtonStates(syncActive);

        setFlag(syncActive)
            .then(() => console.log("Flag set to false."))
            .catch(error => console.error("Flag setting failed.", error));
    });
});

document.getElementById('interval_value').addEventListener('input', updateIntervalOptions);
document.getElementById('interval_value').addEventListener('input', function () {
    let input = this.value;
    this.value = input.replace(/[^0-9]/g, '');
});




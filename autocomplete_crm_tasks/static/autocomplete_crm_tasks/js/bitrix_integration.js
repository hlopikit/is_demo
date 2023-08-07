// В файле лежат 4 функции, вызывающие соответствующие функции в view.

export function finishTasks(finishTasksUrl) {
    return new Promise((resolve, reject) => {
        let checkboxValues = Array.from(document.querySelectorAll('input[name="activity_type"]'))
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);
        let intervalUnit = document.getElementById('interval_unit').value;
        let intervalValue = document.getElementById('interval_value').value;
        fetch(finishTasksUrl, {
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
            .then(response => response.text())
            .then(result => {
                console.log(result);
                resolve();
            })
            .catch(error => {
                console.error(error);
                reject(error);
            });
    });
}

export function initiateAutoFinishLoop(initiateLoopUrl) {
    let checkboxValues = Array.from(document.querySelectorAll('input[name="activity_type"]'))
        .filter(checkbox => checkbox.checked)
        .map(checkbox => checkbox.value);
    let intervalUnit = document.getElementById('interval_unit').value;
    let intervalValue = document.getElementById('interval_value').value;
    fetch(initiateLoopUrl, {
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
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.error(error));
}

export function setFlagState(setFlagUrl, state) {
    return new Promise((resolve, reject) => {
        fetch(setFlagUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams({
                'state': state
            })
        })
            .then(() => resolve())
            .catch(error => {
                console.error(error);
                reject(error);
        });
    });
}


export function getCurrentFlagState(getFlagUrl) {
    return new Promise((resolve, reject) => {
        fetch(getFlagUrl, {
            method: 'GET',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
        })
            .then(response => response.text())
            .then(flagState => {
                let parsedFlagState = flagState === "true";
                resolve(parsedFlagState)
            })
            .catch(error => {
                console.error("Failed to fetch the flag state:", error);
                reject(error);
            })
    })
}

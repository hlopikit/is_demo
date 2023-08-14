export function exportCalls(exportCallsUrl) {
    return new Promise((resolve, reject) => {
        let botToken = document.getElementById('bot_token').value;
        let callsChatId = document.getElementById('calls_chat_id').value;
        fetch(exportCallsUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams({
                'bot_token': botToken,
                'calls_chat_id': callsChatId
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

export function initiateSyncLoop(keepSyncedUrl) {
    let botToken = document.getElementById('bot_token').value;
    let callsChatId = document.getElementById('calls_chat_id').value;
    fetch(keepSyncedUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            'bot_token': botToken,
            'calls_chat_id': callsChatId
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
                console.log("Current flag state is", parsedFlagState)
            })
            .catch(error => {
                console.error("Failed to fetch the flag state:", error);
                reject(error);
            })
    })
}

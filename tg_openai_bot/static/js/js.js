const abstractBotButton = document.getElementById('abstractBotButton');
const standaloneBotButton = document.getElementById('standaloneBotButton');

document.getElementById('abstractBotForm').addEventListener('submit', function (event) {
    event.preventDefault();

    // Заблокируем обе кнопки после отправки запроса
    abstractBotButton.disabled = true;
    standaloneBotButton.disabled = true;

    const formData = new FormData(this);
    console.log(event)
    fetch(this.action, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            // Обработка ответа, если нужно
            if (response.status >= 200 && response.status < 300) {
                // Если запрос выполнен успешно, покажем сообщение об успехе
                document.getElementById('successMessage').style.display = 'block';
            }
        })
});

document.getElementById('standaloneBotForm').addEventListener('submit', function (event) {
    event.preventDefault();

    // Заблокируем обе кнопки после отправки запроса
    abstractBotButton.disabled = true;
    standaloneBotButton.disabled = true;

    const formData = new FormData(this);
    fetch(this.action, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            // Обработка ответа, если нужно
            if (response.ok) {
                // Если запрос выполнен успешно, покажем сообщение об успехе
                document.getElementById('successMessage').style.display = 'block';
            }
        })
});
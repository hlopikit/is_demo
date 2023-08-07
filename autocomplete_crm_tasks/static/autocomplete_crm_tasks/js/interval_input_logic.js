// Текстовое поле выглядит лучше, чем числовое, т.к. у числового сбоку есть ненужные стрелочки.
// Я использую текстовое, но допускаю к вводу только цифры.
document.getElementById('interval_value').addEventListener('input', updateIntervalOptions);
document.getElementById('interval_value').addEventListener('input', function () {
    let input = this.value;
    this.value = input.replace(/[^0-9]/g, '');
});

// Смена формы слова в зависимости от выбранного числа.
// 1 день, 12 дней, 123 дня
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



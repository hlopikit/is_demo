"use strict";

let task_id = ''

BX24.init(function () {
    const response = BX24.placement.info();
    task_id = response.options.taskId;

    let form = document.body.querySelector('form');

    let task_id_field = document.createElement('input');
    task_id_field.setAttribute('type', 'hidden');
    task_id_field.setAttribute('name', 'task_id');
    task_id_field.setAttribute('value', task_id);

    form.appendChild(task_id_field);
});
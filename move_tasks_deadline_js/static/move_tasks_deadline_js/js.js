"use strict";

let BX24_is_loaded = false;
let task_id = ''

BX24.init(function () {
    const response = BX24.placement.info();
    task_id = response.options.taskId;

    BX24_is_loaded = true;
});

function move_tasks_deadline() {
    if (!BX24_is_loaded) {
        console.log("BX24 isnt loaded");
        return;
    }

    BX24.callMethod(
        "tasks.task.get",
        {
            "taskId": task_id,
            "select": ["DEADLINE"]
        },
        function (response) {
            let deadline = response.answer.result.task.deadline;
            if (deadline) {
                deadline = dayjs(deadline);
                deadline = deadline.add(1, 'day');

                BX24.callMethod(
                    "tasks.task.update",
                    {
                        "taskId": task_id,
                        "fields": {"DEADLINE": deadline.format()}
                    }
                );
            }
        }
    );
}
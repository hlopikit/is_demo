def table_for_post(fields):
    """Создает таблицу с данными о лучших звонках менеджеров."""

    table = f"""<table>
                    <tr>
                        <th>№</th>
                        <th>Менеджер</th>
                        <th>ID звонка</th>
                        <th>Номер</th>
                        <th>Запись звонка</th>
                        <th>Длительность</th>
                        <th>Дата</th>
                        <th>Тип</th>
                    </tr>
                    {fields}
                </table>"""

    return table

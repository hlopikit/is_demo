# Generated by Django 4.2.3 on 2023-07-10 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactmp3', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callinfo',
            name='duration',
            field=models.IntegerField(choices=[(0, 'Не уведомлять'), (1, 'Уведомлять')]),
        ),
        migrations.AlterField(
            model_name='callinfo',
            name='type',
            field=models.IntegerField(choices=[(1, 'Исходящий'), (2, 'Входящий'), (3, 'Входящий с перенаправлением'), (4, 'Обратный')]),
        ),
    ]
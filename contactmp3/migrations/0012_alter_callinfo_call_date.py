# Generated by Django 4.2.3 on 2023-07-10 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactmp3', '0011_alter_callinfo_record_url_alter_callinfo_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callinfo',
            name='call_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
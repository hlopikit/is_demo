# Generated by Django 4.2.3 on 2023-07-10 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactmp3', '0008_alter_callinfo_add_to_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callinfo',
            name='record_url',
            field=models.FileField(blank=True, null=True, upload_to='rings/'),
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-07 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_note_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='body',
            field=models.TextField(blank=True, null=True, verbose_name='Note'),
        ),
    ]

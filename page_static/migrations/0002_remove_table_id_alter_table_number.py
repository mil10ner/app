# Generated by Django 4.1.1 on 2022-09-26 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_static', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='id',
        ),
        migrations.AlterField(
            model_name='table',
            name='number',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

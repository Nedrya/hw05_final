# Generated by Django 2.2.19 on 2022-03-14 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20220314_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Название группы'),
        ),
    ]

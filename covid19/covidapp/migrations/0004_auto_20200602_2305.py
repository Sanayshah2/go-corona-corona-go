# Generated by Django 3.0.6 on 2020-06-02 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('covidapp', '0003_auto_20200602_2304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='suggestion',
            options={'ordering': ['-date_posted']},
        ),
    ]
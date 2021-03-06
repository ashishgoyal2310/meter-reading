# Generated by Django 2.0.13 on 2020-07-08 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0002_auto_20200707_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermeter',
            name='configurations',
            field=models.CharField(default='2TB', max_length=32),
        ),
        migrations.AlterField(
            model_name='usermeter',
            name='location',
            field=models.CharField(default=1234, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermeter',
            name='model_type',
            field=models.CharField(default='Storage Device', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermeter',
            name='siteid',
            field=models.CharField(default=9999, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermeter',
            name='warranty',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]

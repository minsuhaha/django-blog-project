# Generated by Django 4.2.5 on 2023-09-14 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='storage',
            field=models.CharField(default='Y', max_length=1),
        ),
    ]
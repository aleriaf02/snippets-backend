# Generated by Django 4.0.2 on 2022-03-14 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0006_rename_snippetfile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='snippet',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]

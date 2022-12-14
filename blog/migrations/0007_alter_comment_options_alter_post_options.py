# Generated by Django 4.1.1 on 2022-11-06 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comment_email_alter_post_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'permissions': (('can_delete_comments', 'Возможность удаления своих комментариев'),), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['date_time'], 'permissions': (('can_delete_posts', 'Возможность удаления своих постов'),), 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
    ]

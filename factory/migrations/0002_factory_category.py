# Generated by Django 3.2.5 on 2021-07-11 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='factory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='factory.factorycategory', verbose_name='カテゴリ'),
        ),
    ]

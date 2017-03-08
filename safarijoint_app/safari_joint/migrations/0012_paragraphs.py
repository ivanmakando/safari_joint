# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-07 14:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import safari_joint.models


class Migration(migrations.Migration):

    dependencies = [
        ('safari_joint', '0011_auto_20170305_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paragraphs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text=b'This is a slide picture upload a picture of size 1600*600 or 1900*750 for home page', null=True, upload_to=safari_joint.models.page_images)),
                ('heading', models.CharField(max_length=500)),
                ('sub_heading', models.CharField(max_length=500)),
                ('content', models.CharField(max_length=90000)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='safari_joint.PageContents')),
            ],
        ),
    ]
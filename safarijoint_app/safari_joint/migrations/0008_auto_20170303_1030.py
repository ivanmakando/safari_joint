# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-03 07:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('safari_joint', '0007_auto_20170302_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccomodationDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_date', models.DateField()),
                ('ending_date', models.DateField()),
                ('ammount_in_percentage', models.FloatField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='safari_joint.PartnersModel')),
            ],
        ),
        migrations.AddField(
            model_name='availableaccomodation',
            name='is_discounted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='accomodationdiscount',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='safari_joint.AvailableAccomodation'),
        ),
    ]
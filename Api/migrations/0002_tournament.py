# Generated by Django 3.1.7 on 2021-03-21 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('data', models.DateField(blank=True)),
                ('participants', models.IntegerField(blank=True)),
                ('mincategory', models.IntegerField()),
                ('maxcategory', models.IntegerField()),
            ],
        ),
    ]
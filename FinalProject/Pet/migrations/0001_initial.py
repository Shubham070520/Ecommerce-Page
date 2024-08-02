# Generated by Django 5.0.7 on 2024-08-02 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('breed', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('age', models.IntegerField()),
            ],
        ),
    ]
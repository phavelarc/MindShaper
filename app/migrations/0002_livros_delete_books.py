# Generated by Django 4.1.3 on 2022-11-23 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomeLivro', models.CharField(max_length=150)),
                ('autor', models.CharField(max_length=150)),
                ('editora', models.CharField(max_length=100)),
                ('ano', models.IntegerField()),
            ],
        ),
    ]

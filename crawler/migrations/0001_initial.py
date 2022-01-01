# Generated by Django 3.2.9 on 2021-12-31 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('handle', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ContestInfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('title_slug', models.CharField(max_length=250)),
                ('start_time', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('title_slug', models.CharField(max_length=250)),
                ('score', models.IntegerField()),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='crawler.contestinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Contestant_Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('timestamp', models.FloatField()),
                ('contestant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attemped', to='crawler.contestant')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solved_by', to='crawler.question')),
            ],
        ),
    ]
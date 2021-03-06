# Generated by Django 2.2.3 on 2019-07-20 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Work Description')),
                ('category', models.CharField(choices=[('ds', 'Designing'), ('wb', 'Web Development'), ('md', 'Medics'), ('ag', 'Agricultural'), ('sa', 'Sys Admin')], max_length=2)),
                ('posted_at', models.DateTimeField(auto_now_add=True, verbose_name='Posted on')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Updated on')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('basework_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='works.BaseWork')),
                ('about_us', models.TextField(blank=True, null=True, verbose_name='About Us')),
            ],
            bases=('works.basework',),
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('basework_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='works.BaseWork')),
                ('expiring_date', models.DateField()),
            ],
            bases=('works.basework',),
        ),
    ]

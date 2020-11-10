# Generated by Django 3.1.3 on 2020-11-09 20:56

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import upload_validator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField(max_length=5000)),
                ('image', models.ImageField(help_text='Only PNG images are accepted', upload_to=blog.models.upload_location, validators=[upload_validator.FileTypeValidator(allowed_extensions=['.png'], allowed_types=['image/png'])])),
                ('datetime_published', models.DateTimeField(auto_now_add=True, verbose_name='datetime published')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='datetime updated')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
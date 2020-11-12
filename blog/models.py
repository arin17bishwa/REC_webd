from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from upload_validator import FileTypeValidator
import datetime


def upload_location(instance, filename, **kwargs):
    file_path = 'blog/{author_id}/{time}-{filename}'.format(
        author_id=str(instance.author.id), time=str(datetime.datetime.now().strftime("%H%M%S%f")), filename=filename
    )
    # print(file_path)
    return file_path


class BlogPost(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location,
                              null=False,
                              blank=False,
                              help_text='Only PNG images are accepted',
                              validators=[FileTypeValidator(allowed_types=['image/png'],
                                                            allowed_extensions=['.png'],
                                                            )]
                              )
    datetime_published = models.DateTimeField(auto_now_add=True, verbose_name='datetime published')
    datetime_updated = models.DateTimeField(auto_now=True, verbose_name='datetime updated')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='liked_by')
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/blog/{}/'.format(self.slug)


@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + '-' + datetime.datetime.now().strftime("%H%M%S%f"))


pre_save.connect(pre_save_blog_post, sender=BlogPost)

from django.db import models
from django.db.models.signals import pre_save, post_delete, post_save, pre_delete
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


class Likes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("BlogPost", on_delete=models.CASCADE)
    liked = models.BooleanField(default=True)

    def __str__(self):
        return '{} likes/dislikes {}'.format(self.user, self.post)


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
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_by', through=Likes)
    like_count = models.PositiveBigIntegerField(default=0)
    dislike_count = models.PositiveBigIntegerField(default=0)
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


@receiver(post_save, sender=Likes)
def modify_count_onsave(sender, instance, created, **kwargs):
    reaction = instance.liked
    qs = BlogPost.objects.filter(pk=instance.post.id)
    obj = qs.first()
    if created:
        if reaction:
            # obj.like_count += 1
            qs.update(like_count=models.F('like_count') + 1)
        else:
            # obj.dislike_count += 1
            qs.update(dislike_count=models.F('dislike_count') + 1)
    else:
        if reaction:
            # obj.like_count += 1
            # obj.dislike_count -= 1
            qs.update(like_count=models.F('like_count') + 1, dislike_count=models.F('dislike_count') - 1)
        else:
            # obj.dislike_count += 1
            # obj.like_count -= 1
            qs.update(dislike_count=models.F('dislike_count') + 1, like_count=models.F('like_count') - 1)
    # obj.save()


@receiver(pre_delete, sender=Likes)
def modify_count_ondel(sender, instance, **kwargs):
    reaction = instance.liked
    qs = BlogPost.objects.filter(pk=instance.post.id)
    obj = qs.first()
    if reaction:
        # obj.like_count -= 1
        qs.update(like_count=models.F('like_count') - 1)
    else:
        # obj.dislike_count -= 1
        qs.update(dislike_count=models.F('dislike_count') - 1)
    # obj.save()

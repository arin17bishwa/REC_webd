from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound, Http404
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.conf import settings
from blog.models import BlogPost
from blog.forms import (CreateBlogPostForm,
                        UpdateBlogPostForm,
                        )
from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

BLOG_POSTS_PER_PAGE = settings.BLOG_POSTS_PER_PAGE

Account = User
#qwert@123

@login_required(login_url='/account/must-authenticate')
def create_blog_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('account:must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(username=user.username).first()
        obj.author = author
        obj.save()
        return redirect('home')
    context['form'] = form

    return render(request, 'blog/create_blog.html', context)


@login_required(login_url='/account/must-authenticate')
def detail_blog_view(request, slug):
    context = {}

    try:
        blog_post = get_object_or_404(BlogPost, slug=slug)
    except Exception as e:
        return HttpResponseNotFound()

    context['blog_post'] = blog_post

    return render(request, 'blog/detail_blog.html', context)


@login_required(login_url='/account/must-authenticate')
def edit_blog_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('account:must_authenticate')

    try:
        blog_post = get_object_or_404(BlogPost, slug=slug)
    except Http404 as e:
        return HttpResponseNotFound('Exception:{}'.format(e))

    if blog_post.author != user:
        return HttpResponseForbidden()

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            # blog_post = obj
            context['success_message'] = 'Successfully Updated'
            return redirect('home')
    form = UpdateBlogPostForm(
        initial={
            'title': blog_post.title,
            'body': blog_post.body,
            'image': blog_post.image,
        }
    )

    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)


@login_required(login_url='/account/must-authenticate')
def delete_blog_view(request, slug):
    context = {}
    user = request.user
    try:
        blog_post = get_object_or_404(BlogPost, slug=slug)
    except Exception as e:
        return HttpResponseNotFound()

    if blog_post.author != user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        blog_post.delete()
        # print('dednt delete {}'.format(blog_post))
        return redirect('home')

    context['post'] = blog_post
    return render(request, 'blog/confirm_del.html', context)


@login_required(login_url='/account/must-authenticate')
def home_screen_view(request):
    context = {}

    blog_posts = BlogPost.objects.all().order_by('-datetime_updated')

    # Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts
    return render(request, 'blog/home.html', context)

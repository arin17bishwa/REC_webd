from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound, Http404, JsonResponse,HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.conf import settings
from blog.models import BlogPost, Likes, Comment
from blog.forms import (CreateBlogPostForm,
                        UpdateBlogPostForm,
                        CommentForm
                        )
from .templatetags import extra_filters
from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from rest_framework.decorators import api_view
from django.utils.timezone import make_aware
from datetime import datetime
from collections import defaultdict
from urllib.parse import quote_plus
BLOG_POSTS_PER_PAGE = settings.BLOG_POSTS_PER_PAGE
LOGIN_URL = settings.LOGIN_URL

Account = User


# qwert@123

@login_required
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


@login_required
def detail_blog_view(request, slug):
    context = {}

    try:
        blog_post = get_object_or_404(BlogPost, slug=slug)
    except Exception as e:
        return HttpResponseNotFound()

    reacted = Likes.objects.filter(user=request.user.id, post=blog_post.id)
    context['liked'] = reacted.filter(liked=True).exists()
    context['disliked'] = reacted.filter(liked=False).exists()
    context['blog_post'] = blog_post
    context['share_quote']=quote_plus(blog_post.title)
    all_comments = Comment.objects.filter(post=blog_post.id)
    comments = all_comments.filter(parent=None).order_by('-timestamp')
    replies = all_comments.exclude(parent=None).order_by('-timestamp')
    rep_d = defaultdict(list)
    for reply in replies:
        rep_d[reply.parent.id].append(reply)
    context['comments'] = comments
    context['replies'] = rep_d
    # print(rep_d)

    return render(request, 'blog/detail_blog.html', context)


@login_required
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


@login_required
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


@login_required
def home_screen_view(request):
    context = {}
    blog_posts = BlogPost.objects.all()
    data = request.GET
    start = data.get('start', False)
    end = data.get('end', False)

    if start and end:
        start_date = make_aware(datetime.strptime(start, '%Y-%m-%d'))
        end_date = make_aware(datetime.strptime(end, '%Y-%m-%d'))
        blog_posts = blog_posts.filter(datetime_published__gte=start_date).filter(datetime_published__lte=end_date)

    blog_posts = blog_posts.order_by('-datetime_updated')

    # region Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    # endregion

    context['blog_posts'] = blog_posts
    return render(request, 'blog/home.html', context)


@api_view(['POST', ])
@login_required
def action_view(request):
    data = request.data

    try:
        user = get_object_or_404(User, id=data.get('userId'))
    except Http404 as e:
        return HttpResponseNotFound()

    try:
        post = get_object_or_404(BlogPost, id=data.get('postId'))
    except Http404 as e:
        return HttpResponseNotFound()

    action = data.get('action')
    obj, created = Likes.objects.get_or_create(user=user, post=post)
    # print(obj, created)
    liked = True
    disliked = False
    if action:  # pressed like button
        if not created:
            if obj.liked:  # Unliking
                obj.delete()
                liked = False
            else:
                obj.liked = True  # means Liked now(previously disliked)
                obj.save()
                liked = True
    # region Press Dislike button
    # else:  # pressed Dislike button
    #     if created:
    #         obj.liked = False
    #         obj.save()
    #         liked = False
    #         disliked = True
    #     else:
    #         if obj.liked:
    #             obj.liked = False
    #             obj.save()
    #             disliked = True
    #             liked = False
    #
    #         else:
    #             obj.delete()
    #             # print('dislike removed')
    #             liked = False
    # endregion
    # region Dislike button HTML portion
    # {  # <div style="display:inline; float:right">#}
    #     {  # <div id="{{ blog_post.id }}-dislike">#}
    #         {  # {% if disliked %}#}
    #             {
    #                 # <i onclick="handleAction({{ blog_post.id }},{{ request.user.id }},0)" class="fa fa-thumbs-down">Disliked!</i>#}
    #                 {  # {% else %}#}
    #                     {
    #                         # <i onclick="handleAction({{ blog_post.id }},{{ request.user.id }},0)" class="fa fa-thumbs-o-down">Dislike</i>#}
    #                         {  # {% endif %}#}
    #                             {  # </div>#}
    #                                 {  # <div id="dislike-count-{{ blog_post.id }}" class="dislike-count" >#}
    #                                     {  # {{ blog_post.dislike_count }} Dislikes#}
    #                                         {  # </div>#}
    #                                             {  # </div>#}
    # endregion
    post.refresh_from_db()
    context = {
        'likes': post.like_count,
        'dislikes': post.dislike_count,
        'liked': liked,
        'disliked': disliked,
    }
    print(context)
    return JsonResponse(data=context, content_type='application/json')


@api_view(['POST', ])
@login_required
def post_comment_view(request):
    form = CommentForm(request.POST or None)
    # print(1111111,'\n',request.POST)
    postId = request.POST.get('postId')
    # print(postId)
    post = BlogPost.objects.get(id=postId)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.post = post
        parent_id = request.POST.get('parent', '')
        if parent_id != '':
            parent_comm = Comment.objects.get(id=parent_id)
            if parent_comm.depth>=3:
                return HttpResponseBadRequest(content='Max Thread limit exceeded')
            obj.parent = parent_comm

        obj.save()

    return redirect('blog:detail', slug=post.slug)

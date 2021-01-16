from django.urls import path
from blog.views import (
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
    delete_blog_view,
    action_view,
    post_comment_view,
)

app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name='create'),
    path('<slug>/', detail_blog_view, name='detail'),
    path('<slug>/edit', edit_blog_view, name='edit'),
    path('<slug>/delete', delete_blog_view, name='delete'),
    path('react', action_view, name='react'),
    path('postComment',post_comment_view,name='post_comment')
]


"""
        {% for comment in comments %}
            <div class="row my-3">
                <div class="col-md-1 bg-success">
                    <img src="{%static 'tsubaki.png' %}" alt="An image" class="rounded  mx-auto d-block p-2" height="60" width="60">
                </div>
                <div class="col-md-11 bg-warning">
                    <b>{{ comment.user.username }}</b> on {{ comment.timestamp|localtime }}
                    <div>{{ comment.content }}</div>
                    <div class="reply mx-0">
                        <button class="btn btn-sm btn-primary" type="button" data-toggle="collapse" data-target="#commentReply-{{ comment.id }}" aria-expanded="false" aria-controls="commentReply-{{ comment.id }}">
                            Reply
                        </button>
                        <div class="collapse" id="commentReply-{{ comment.id }}">
                            <div class="card card-body my-2">
                                <form action="{% url 'blog:post_comment' %}" method="post">{% csrf_token %}
                                    <div class="form-group">
                                        <label for="content">Post reply</label>
                                        <input type="text" class="form-control" name="content" placeholder="Enter comment...">
                                    </div>
                                    <input type="hidden" name="postId" value="{{ blog_post.id }}">
                                    <input type="hidden" name="parent" value="{{ comment.id }}">
                                    <button type="submit" class="btn btn-primary">Submit</button>
                                </form>
                            </div>
                        </div>
                    </div>


                </div>
            </div>
        {% endfor %}


"""










'''




/* Add a black background color to the top navigation */
.topnav {
  background-color: #f2f2f2;
  overflow: hidden;
}

/* Style the links inside the navigation bar */
.topnav a {
  float: left;
  display: block;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

/* Change the color of links on hover */
.topnav a:hover {
  background-color: #ddd;
  color: black;
}

/* Add an active class to highlight the current page */
.topnav a.active {
  background-color: #4CAF50;
  color: white;
}

/* Hide the link that should open and close the topnav on small screens */
.topnav .icon {
  display: none;
}

'''



'''
        <div class="date-filter">
            <form method="get">{% csrf_token %}
                <div style="float: left">
                    <label for="id_start">Start</label>
                    <input class="form-control" type="date" name="start" id="id_start" placeholder="Start Date" required autofocus/>
                </div>
                <div style="float: right">
                    <label for="id_end">End</label>
                    <input class="form-control" type="date" name="end" id="id_end" placeholder="End Date" required autofocus/>
                </div>
                <button type="submit">Filter</button>
            </form>
        </div>

'''
from django.urls import path
from blog.views import (
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
    delete_blog_view,
    action_view,
)

app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name='create'),
    path('<slug>/', detail_blog_view, name='detail'),
    path('<slug>/edit', edit_blog_view, name='edit'),
    path('<slug>/delete', delete_blog_view, name='delete'),
    path('react', action_view, name='react'),
]
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
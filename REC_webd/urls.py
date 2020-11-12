from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# added by me

from blog.views import (
    home_screen_view,
)

urlpatterns = [
    path('', home_screen_view, name='home'),
    path('account/', include('account.urls'), name='account'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', 'blog')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''
<div class="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm">
  <h5 class="my-0 mr-md-auto font-weight-normal">
    {%if request.user.is_authenticated%}
    Hello, {{request.user.username}}
    {%endif%}
  </h5>


  <nav class="my-2 my-md-0 mr-md-3">
    {%if request.user.is_authenticated%}
        <p>
            <a class="p-2 text-dark" href="{%url 'home'%}">HOME </a>
            <a class="p-2 text-dark" href="{%url 'account:logout'%}">Logout </a>
        </p>
    {%else%}
        <p>
            <a class="p-2 text-dark" href="{%url 'home'%}">HOME </a>
            <a class="p-2 text-dark" href="{%url 'account:login'%}">Login </a>
            <a class="btn btn-outline-primary"  href="{%url 'account:register'%}"> Register</a>
        </p>
    {%endif%}

  </nav>
</div>

'''


'''
<nav class="topnav fixed-top navbar" id="myTopnav">


    <h5 class="my-0 mr-md-auto font-weight-normal text-center">
    {%if request.user.is_authenticated%}
    Hello, {{request.user.username|capfirst}}
    {%endif%}
    </h5>


    {%if request.user.is_authenticated%}
        <p>
            <a class="p-2 text-dark" href="{%url 'home'%}">HOME </a>
            <a class="p-2 text-dark" href="{%url 'account:logout'%}">Logout </a>
        </p>
    {%else%}
        <p>
            <a class="p-2 text-dark" href="{%url 'home'%}">HOME </a>
            <a class="p-2 text-dark" href="{%url 'account:login'%}">Login </a>
            <a class="p-2 text-dark" href="{%url 'account:register'%}"> Register</a>
        </p>
    {%endif%}
    <p>
        <a href="javascript:void(0);" class="icon" onclick="myFunction()">
            <i class="fa fa-bars"></i>
        </a>
    </p>




</nav>

'''
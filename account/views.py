from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.
# qwert@123
def registration_view(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_ = form.save(commit=True)
            user_.set_password(form.cleaned_data.get('password1'))
            user_.save()
            # print(form.cleaned_data)
            if user_:
                login(request, user_)
                return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = UserCreationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST or None)
        if form.is_valid():
            user_ = form.get_user()
            if user_:
                login(request, user_)
                return redirect('home')
    else:
        form = AuthenticationForm()
    context['login_form'] = form

    return render(request, 'account/login.html', context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html')

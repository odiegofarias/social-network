from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register_view(request):
    template = 'conta/register_user.html'

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            return redirect('conta:login-view')

    else:
        form = RegisterForm()

    context = {'form': form}

    return render(request, template, context)


def login_view(request):
    template = 'conta/login.html'

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data.get('username', ''),
                password = form.cleaned_data.get('password', ''),
            )

            if user is not None:
                messages.success(request, 'Login feito com sucesso')
                login(request, user)

                return redirect('posts:main-post-view')
            else:
                messages.error(request, 'Credenciais inválidas')
        else:
            messages.error(request, 'Usuário ou senha incorreto.')
            
            return redirect('conta:login-view')

    form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, template, context)


def logout_view(request):
    logout(request)

    return redirect('conta:login-view')
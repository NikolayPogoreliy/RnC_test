from django.shortcuts import render, redirect, reverse


def login_view(request):
    if request.user.is_authenticated:
        return redirect('api/')
    return render(request, 'login.html')

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse

from django.views import View
from utils.resultful import ResultCode


class Login(View):
    def get(self, request):
        return render(request, 'backend/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return ResultCode.ok()
        return ResultCode.params_error()


def logout_view(request):
    logout(request)
    return redirect(reverse('userauth:login'))


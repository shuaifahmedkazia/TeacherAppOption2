from django.shortcuts import render
from django.contrib.auth import logout
from django.views import View

class IndexView(View):
    def get(self, request, *args, **kwargs):
         return render(request,'login.html',{})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request,'login.html',{})

    
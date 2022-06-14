"""TeacherDirectory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TeacherDirectory import views as mainView
from directory import views as dt
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', mainView.IndexView.as_view(), name='login'),
    path('logout/', mainView.LogoutView.as_view(), name='logout'),
    path('Login/',dt.LoginView.as_view(), name='Login'),
    path('importedForm/', dt.ImoportFormView.as_view(), name='importedForm'),
    path('GetProfilePage/', dt.GetProfilePageView.as_view(), name='GetProfilePage'),
    path('DataView/', dt.AllTeacherDataView.as_view(), name='DataView'),
    path('AddTeacherData/', dt.AddTeacherDataView.as_view(), name="AddTeacherData"),
    path('apphome/',dt.apphome, name='apphome'),  
    path('importBulk/',dt.ImportBulkView.as_view(), name='importBulk'),


   
 
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
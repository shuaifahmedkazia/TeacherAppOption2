import json
from django.shortcuts import render
from django.contrib import messages
from .models import SubjectsModel, TeacherModel
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

class LoginView(View):
    def post(self, request, *args, **kwargs):
        loginid = request.POST.get('username')
        pswd = request.POST.get('password')

        try:
            user = authenticate(request, username=loginid, password=pswd)
            
            if user is not None: 
                login(request, user)
         
                qs = TeacherModel.objects.all()
        
                return render(request, 'AllData.html', {'data': qs})
            else:
                messages.success(request, 'invalid Credential')
                return render(request, 'login.html')
        except Exception as e:
         
            pass
        messages.success(request, 'Invalid Login id and password')
        return render(request, 'login.html')
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {})


class ImoportFormView(View):
    @method_decorator(login_required(login_url='/Login/'))
    def get(self, request, *args, **kwargs):
        return render(request, 'importerform.html', {})


class GetProfilePageView(View):
    @method_decorator(login_required(login_url='/Login/'))
    def get(self, request, *args, **kwargs):
        id = int(request.GET.get('uid'))
        data = TeacherModel.objects.get(id=id)
        return render(request, 'ProfilePage.html', {'data': data})



class AllTeacherDataView(View):
    @method_decorator(login_required(login_url='/Login/'))
    def get(self, request, *args, **kwargs):
        qs = TeacherModel.objects.all()
  
        return render(request, 'AllData.html', {'data': qs})

    @method_decorator(login_required(login_url='/Login/'))
    def post(self, request, *args, **kwargs):
        filtertxt = request.POST.get('filtertext')
        data = TeacherModel.objects.filter(Q(LastName__icontains=filtertxt) |Q(Subjectstaught__Subjectstaught__icontains=filtertxt))
        return render(request, 'AllData.html', {'data': data})


class AddTeacherDataView(View):
    def get(self, request, *args, **kwargs):
        qs = SubjectsModel.objects.all()
        return render(request, 'AddTeacherData.html', {'data':qs})

    def post(self, request, *args, **kwargs):
        results = request.POST.getlist('subject[]')
       
        for res in results:
            r = SubjectsModel.objects.get(id=int(res))
      
       
        
        filename = ""
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage("media/profilepic")
            filename = fs.save(myfile.name, myfile)
        except:
            filename= "default.jpg"
        
        
        

        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        roomnumber = request.POST.get('roomnumber')
       

        sub = len(results)
        if sub <= 5:
            try:
                newteacher = TeacherModel(FirstName=firstName, LastName=lastName, Profilepicture=filename,
                                            EmailAddress=email, PhoneNumber=mobile, RoomNumber=roomnumber)
                newteacher.save()

                for res in results:
                    r = SubjectsModel.objects.get(id=int(res))
                    newteacher.Subjectstaught.add(r)
                
                

            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'subjectcannot contain more than 5')
            
        qs = TeacherModel.objects.all()
        return render(request, 'AllData.html', {'data': qs,'class':'alert-danger'})


def apphome(request):
    return render(request, 'apphome.html', {})

  


def checkData():
    import os
    li = []
    for x in os.listdir(settings.MEDIA_ROOT + "\\" + "profilepic"):
        if x.endswith(".JPG") or x.endswith(".jpg"):
            li.append(x)
    return li




class ImportBulkView(View):
    def get(self, request, *args, **kwargs):
        TeacherModel.objects.all().delete()
        path = settings.MEDIA_ROOT + "\\" + "Teachers.csv"
        import pandas as pd
        df = pd.read_csv(path, encoding='utf-8')
        li = checkData()
     
        for i in df.index:
            FirstName = df['First Name'][i]
            LastName = df['Last Name'][i]
            Profilepicture = df['Profile picture'][i]
            EmailAddress = df['Email Address'][i]
            PhoneNumber = df['Phone Number'][i]
            RoomNumber = df['Room Number'][i]
            Subjectstaught = df['Subjects taught'][i]

            pic = 'default.jpg'
            if Profilepicture not in li:
                Profilepicture = pic

            # l2 = len(FirstName)
            sub = Subjectstaught.split(', ')
            subjects = Subjectstaught.split(',')
           
            sub = len(sub)
            if sub <= 5:
                newteacher = TeacherModel.objects.create(FirstName=FirstName, LastName=LastName, Profilepicture=Profilepicture,
                                            EmailAddress=EmailAddress, PhoneNumber=PhoneNumber, RoomNumber=RoomNumber)
                
                newteacher.save()

                for res in subjects:
                    res = res.lower()
                    res = res.strip()
                  
                    r = SubjectsModel.objects.get(Subjectstaught=res)
                 
                    newteacher.Subjectstaught.add(r)


        messages.success(request, 'Data Imported')
        return render(request, 'importerform.html', {})

    def post(self, request, *args, **kwargs):
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)

            
        
            path = settings.MEDIA_ROOT + "\\" + filename

            import pandas as pd
            df = pd.read_csv(path, encoding='utf-8')
            li = checkData()
            data_added = 0
            data_skipped = 0
            subject_not_found = 0
            for i in df.index:
                FirstName = df['First Name'][i]
                LastName = df['Last Name'][i]
                Profilepicture = df['Profile picture'][i]
                EmailAddress = df['Email Address'][i]
                PhoneNumber = df['Phone Number'][i]
                RoomNumber = df['Room Number'][i]
                Subjectstaught = df['Subjects taught'][i]

                pic = 'default.jpg'
                if Profilepicture not in li:
                    Profilepicture = pic

               
                sub = Subjectstaught.split(',')
                subjects = Subjectstaught.split(', ')
           
                sub = len(sub)
                if sub <= 5:
                    try:
                        newteacher = TeacherModel.objects.create(FirstName=FirstName, LastName=LastName, Profilepicture=Profilepicture,
                                            EmailAddress=EmailAddress, PhoneNumber=PhoneNumber, RoomNumber=RoomNumber)
                
                        newteacher.save()
                        
                        for res in subjects:
                            res = res.lower()
                            res = res.strip()
                  
                            r = SubjectsModel.objects.filter(Subjectstaught=res).first()
                            if r is not None:
                                newteacher.Subjectstaught.add(r)
                            else:
                                subject_not_found +=1


                        data_added +=1
                    except:
                        data_skipped +=1
                        pass

            messages.success(request, str(data_added)+' Data Imported and ' +str(data_skipped)+' Data Skipped Due to Value error or duplicate entry'+str(subject_not_found)+" subject not linked to any teacher due to unavailablity ")
            return render(request, 'importerform.html', {})




        
        










        
        
     

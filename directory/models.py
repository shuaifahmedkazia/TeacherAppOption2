from django.db import models

# Create your models here.
class LoginTable(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'LoginTable'

class SubjectsModel(models.Model):
    Subjectstaught = models.CharField(max_length=100)
    def __str__(self):
        return self.Subjectstaught

    class Meta:
        db_table = 'Subjects'

class TeacherModel(models.Model):
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Profilepicture = models.CharField(max_length=100)
    EmailAddress = models.CharField(unique=True, max_length=100)
    PhoneNumber = models.CharField(max_length=100)
    RoomNumber = models.CharField(max_length=100)
    Subjectstaught = models.ManyToManyField(SubjectsModel)
    def __str__(self):
        return self.LastName

    class Meta:
        db_table = 'Teachers'

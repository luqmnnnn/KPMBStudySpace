from django.db import models

class User(models.Model):
    userID = models.CharField(max_length=11, primary_key=True)
    userName = models.CharField(max_length=100)
    userEmail = models.CharField(max_length=320)
    userMobile = models.CharField(max_length=11)
    password1 = models.TextField()
    password2 = models.TextField()

class TuitionPackage(models.Model):
    tuitionPackageID = models.CharField(max_length=6, primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    packageCategory = models.CharField(max_length=100)
    packageDescription = models.TextField()
    packagePrice = models.DecimalField(max_digits=6, decimal_places=2)
    subjects = models.CharField(max_length=100)

class Registration(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    registrationID = models.CharField(max_length=6, primary_key=True)
    registrationPlace =models.TextField()
    session = models.CharField(max_length=10)
    registrationPrice = models.DecimalField(max_digits=6, decimal_places=2, default=000000.00)
    status = models.CharField(max_length=10, default='Not Ready')
    time = models.DateTimeField(auto_now_add=True)
class Suggestion(models.Model):
    userID= models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    forum = models.TextField()
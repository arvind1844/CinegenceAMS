import email
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your models here.
class Assests(models.Model):
    title=models.CharField(max_length=255)
    image =models.ImageField(upload_to='images/assests',null=True,blank=True)
    content=models.CharField(max_length=30,verbose_name="Short text about the asset. Max 30 words.")
    description=models.TextField(blank=True,null=True)
    is_approved = models.BooleanField(
        default=False, verbose_name="Approve this to remove assest from website")

    def __str__(self):
        return self.title 

class IndividualAssest(models.Model):
    assest = models.ForeignKey(Assests, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/assests', default=None)
    

    class Meta:
        verbose_name = "Assest Image"
        verbose_name_plural = "Assest Images"

    def __str__(self):
        return self.assest.title

class ExtendedUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    contact_number = models.BigIntegerField(null=True, blank=True)
    address = models.TextField(null=True)
    email = models.EmailField(null = True,unique=True)

    def __str__(self):
        return str(self.name)

class Work_Details(models.Model):
    def resume_path(self,id):
        return f'{self.user.id}/'
    user=models.ForeignKey(ExtendedUser , null=True, blank=True,on_delete=models.SET_NULL)
    assest = models.ForeignKey(Assests, on_delete=models.CASCADE,null = True)
    worklink=models.CharField(max_length=255,null=True, blank=True)
    aadhar=models.BigIntegerField(null=True, blank=True)
    resume=models.FileField(null=True, blank=True,upload_to=resume_path)
    is_selected = models.BooleanField(
        default=False, verbose_name="Approve this to select the applicant")

    def save(self,*args,**kwargs):
        if self.is_selected:
            send_mail('You are selected for' + str(self.assest)+ 'assest', 'Hello applicant', 'sender email will come here', [self.user.email], fail_silently=False)
            self.assest.is_approved = True
            self.assest.save()
        return super().save(*args,**kwargs)

    def __str__(self):
        return str(self.user)

class Contact(models.Model):
    user=models.ForeignKey(ExtendedUser , null=True, blank=True,on_delete=models.SET_NULL)
    email=models.EmailField(max_length=255,null=True, blank=True)
    subject=models.CharField(max_length=800,null=True, blank=True)
    message=models.CharField(max_length=1000,null=True, blank=True)

    def __str__(self):
        return str(self.email)




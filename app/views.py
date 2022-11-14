import os
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.contrib.auth.models import User 
from django.core.files.storage import FileSystemStorage
from frontend.settings import MEDIA_ROOT
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('register')

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        if 'submit-signup' in request.POST:
            name = request.POST.get('username')
            contact_no = request.POST.get('contact')
            email = request.POST.get('email')
            address = request.POST.get('address')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if  User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists! Use another email to register.')
                return redirect('/register/')
            if password1 != password2:
                messages.error(request, 'Password did not match, please try again')
                return redirect('/register/')
            user = User.objects.filter(email=email).first()

            if user == None:
                user = User.objects.create_user(username=email, email=email, password=password1)
                eu = ExtendedUser.objects.create(user=user,name=name, contact_number=contact_no, address=address, email=email)
                messages.success(request, 'Registered successfully!')                
                return redirect('/register/')
                            
        elif 'submit-login' in request.POST:
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            user = authenticate(username=email, password=password1)
            print(user)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('/')
            else:
                messages.error(request, 'Username or password incorrect')
                return redirect('/register/')
    return render(request,'user.html')


# def change_password(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             old_password = request.POST.get ( 'old_password' )
#             new_password1 = request.POST.get ( 'new_password1' )
#             new_password2 = request.POST.get ( 'new_password2' )
#             print('request',request.user.password)

#             user = authenticate ( username=request.user.username, password=old_password )


#             if new_password1 != new_password2:
#                 messages.warning ( request, 'password did not match' )
#                 return redirect ( '/password_change/' )

#             if user is not None:
#                 user.password = make_password ( new_password1 )
#                 user.save ()
#                 # messages.success ( request, 'Your password was successfully updated!' )
#                 print ( request.user.is_authenticated )
#                 return redirect ( 'home' )
#             else:
#                 return render ( request, 'accounts/error-404.html' )
#         else:
#             return render ( request, 'accounts/error-404.html' )
#     else:
#         return render ( request, 'accounts/error-404.html' )






#Update Profile
@login_required(login_url='/register/')
def UpdateProfileView(request):
    context = {}
    
    if request.method == 'POST':
        # user = request.user
        # print(user.id)
        name = request.POST.get ( 'username' )
        contact_no = request.POST.get ( 'contact' )
        email = request.POST.get ( 'email' )
        address = request.POST.get ( 'address' )
        user = ExtendedUser.objects.get(email=email)
        # print(user)
      
        name = user.name
        contact_no = user.contact_number
        address =  user.address
        # user.update(name=name,contact_number=contact_no,address=address,email=email)
   
        user.save(update_fields=['name','email','contact_number','address'])
        messages.success(request,'Profile updated successfully! ')
        return redirect('/user_profile/')
    else:
        user = ExtendedUser.objects.filter(email=request.user).first()
        work=Work_Details.objects.filter(user=user)
        return render(request,'user_profile.html', {'work':work,'name':user.name,'address':user.address,'contact':user.contact_number,'email':user.email, 'nbar':'user_profile'})

def home(request):
    asset=Assests.objects.filter(is_approved=False).order_by('-id')[:3]
    return render(request,'index.html',{'asset':asset,'nbar':'home'})

def logout_view(request):
    logout ( request )
    return redirect ( "/" )

def terms(request):
    return render(request,'terms.html')

@login_required(login_url='/register/')
def individual_asset(request,id):
    asset=Assests.objects.filter(id=id).first()
    print(asset)
    one_asset=IndividualAssest.objects.filter(assest=asset)
    context={'one_asset':one_asset,'assest':asset}
    return render(request,'assets_single.html',context)

@login_required(login_url='register')
def all_assets(request):
    asset=Assests.objects. filter(is_approved=False)
    paginator = Paginator(asset, 6)
    page = request.GET.get('page',1)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'all_assets.html',{'asset':asset,'users':users,'nbar': 'all_assests'})

@login_required(login_url='register')
def form_details(request,id):
    if request.method=='POST':
        aadhar=request.POST.get('aadhar')
        work_link=request.POST.get('work')
        resume=request.FILES.get('resume')
        print(resume)
        eu =ExtendedUser.objects.filter(user=request.user).first()
        assest = Assests.objects.filter(id=id).first()
        work=  Work_Details.objects.create(assest=assest,user=eu,aadhar=aadhar,worklink=work_link,resume="")
       
        if resume:
            fileStorage = FileSystemStorage(location=os.path.join(MEDIA_ROOT,str(request.user.id)))
            print(fileStorage)
            resume_file = fileStorage.save(resume.name, resume)
            work.resume = f'{request.user.id}/' + str(resume_file)
            work.save()
        
        messages.success(request,'Thank you for applying, you will recieve a mail soon.')

        return redirect('/individual_asset/'+ id)
    



@login_required(login_url='/register/')
def contact(request):
    if request.method=='POST':
        name=request.POST.get('username')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        eu =ExtendedUser.objects.get(user=request.user)
        print(eu)
        # contact=Contact.objects.create(user=eu,email=email,subject=subject,message=message)
        
        messages.success(request,'Message sent')
        return redirect('/contact/')
      
    else:
        return render(request,'contact.html')



@login_required(login_url='/register/')
def timer(request,id):
    asset = Assests.objects.filter(id=id).first()
    time=asset.timeStamp.strftime("%Y-%m-%dT%H:%M:%S")   
    context={'time':time}
    return render(request,'timer.html',context)

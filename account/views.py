from django.contrib.auth import authenticate, login as authlogin ,logout  as authlogout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Account
from .forms import AccountCreate, UpdateUserForm, CreateProfile
from django.contrib.sites.shortcuts import get_current_site
import random
from django.core.mail import send_mail
from django.conf import settings
from projectfund.models import Project





def signup(request):
    if request.method == "POST":
        form = AccountCreate(request.POST, request.FILES)
        if form.is_valid():
            acc = Account()
            email = form.cleaned_data['email']
            uname = request.POST['firstname'] + " " + request.POST['lastname']
            user = User.objects.create_user(username=uname, email=request.POST['email'],
                                     password=request.POST['password'],
                                     is_superuser=True, is_staff=True)
            domain_name = get_current_site(request).domain
            token = str(random.random()).split('.')[1]
            acc.token = token
            acct = form.save(commit=False)
            acct.token = token
            acct.save()
            link = f'http://{domain_name}/verify/{token}'
            send_mail(
                'Email verification',
                f'plz clik this link {link} to verify your mail',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return HttpResponse('Please confirm your email address to complete the registration')
            # return redirect(('accounts/profile'))
    else:
        form = AccountCreate()
    context = {"form": form}
    return render(request,'account/signup.html',context)


def verify(request,token):
    try:
        user = Account.objects.get(token=token)
        if user:
            print(user)
            print(user.email)
            user.is_active = True
            user.save()
            msg = "your email is active"
            print(msg)
        return render(request, 'account/login.html', {"msg": msg})
    except Exception as e:
        msg = e
        return render(request, 'account/success.html', {"msg": msg})


def signin(request):
    if (request.session.get('email') is None):
            if (request.method=='GET'):
                return render(request,'account/login.html')
            else:
                User = Account.objects.filter(email=request.POST['email'],password=request.POST['password'])
                if len(User)>0 and User is not None:
                    username = User[0].firstname + " " + User[0].lastname
                    authuser = authenticate(username=username, password=request.POST['password'])
                    request.session['email'] = User[0].email
                    authlogin(request, authuser)
                    return redirect('account:users_profile',id=User[0].id)
                context={}

                context['Erorr'] ='invalid Email or Password'
                return redirect('account:signup',)
    else:
      return redirect('projectfund:home')

def logout(request):
    print('before logout')
    print(request.session.get('email'))
    if request.user.is_authenticated:
        print('if logout')
        request.session.clear()
        authlogout(request)
    return redirect('projectfund:home')

def deletepage(request,id):
    deleteuser= Account.objects.get(id=id)
    return render(request, 'account/DeleteAccount.html',{'deleteuser':deleteuser})

def deleteAccount(request,id):
        deleteuser = Account.objects.get(id=id)
        print(deleteuser.firstname)
        deleteuser.delete()

        return render(request,'fack/log-in.html')


@login_required
def updateuser(request, id):
    if request.method == 'POST':
        account = Account.objects.get(id=id)
        email = account.email
        form = UpdateUserForm(data=request.POST, files=request.FILES, instance=account)
        username = request.POST['firstname']+request.POST['lastname']
        if form.is_valid():
            form.save()
            User.objects.filter(email=email).update(username=username)
            return HttpResponse("data is updated")
    else:
        form = UpdateUserForm()
    context = {'form': form}
    return render(request,'account/updateuser.html', context)


@login_required
def addprofile(request,id):
    if request.method == 'POST':
        account = Account.objects.get(id=id)
        form = CreateProfile(data=request.POST)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.name = account
            acc.save()
            return HttpResponse("profile is created")
    else:
        form = CreateProfile()
    context = {'form': form,}
    return render(request,'account/addprofile.html', context)

def profile(request, id):
    context = {}
    context['account'] = Account.objects.get(id=id)
    return render(request, 'account/profile.html', context)



def view_projects(request,id):
    context = {}
    views =Account.objects.get(id=id)
    context['account'] = Project.objects.filter(creator_id=views.id)
    print(context)
    return render(request, 'account/viewproject.html', context)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Project, ProjectTag, ProjectImage
from .forms import FormDonate, CreateProject, ImageProjectFrom, ProjectTagForm
from account.models import Account
from .forms import FormDonate
from datetime import datetime
from .models import *
from django.shortcuts import render, get_object_or_404
from .forms import *




def list_project(request):
    projects = Project.objects.all()
    return render(request, 'projectfund/projects.html',{'projects':projects})


def detail_project(request, id):
    project = Project.objects.get(id=id)
    tag = ProjectTag.objects.filter(project_name_tag=project)
    image = ProjectImage.objects.filter(project_name=project)
    countt = Rate.objects.filter(ratee=project)
    comment = Comment.objects.filter(proj=project)
    account1 = User.objects.get(username=request.user)
    account = Account.objects.get(email=account1.email)
    count_rate = countt.count()
    total = 0
    for i in countt:
        total = total + int(i.rating)
    try:
         avrg_rate = total / count_rate
    except Exception:
        avrg_rate = 'no rate here'
    datetoday = datetime.now().date()
    min = int(project.total_target) * 0.25
    if request.method == "POST":
        if project.start_date == datetoday and float(project.donations) < min:
            print('cancel project')
            project.delete()
            return render(request, 'base.html')
        else:
            print(project.donations)
        if int(project.donations) < int(project.total_target):
             request.POST._mutable = True
             request.POST['donations'] = str(int(request.POST['donations']) + int(project.donations))
             form = FormDonate(data=request.POST, files=request.FILES, instance=project)
             request.POST._mutable = False
             if form.is_valid():
                 form.save()
                 form = FormDonate()
                 msg = ''
                 Donation.objects.create(pro=project,acc=account,donation_account_project=request.POST['donations'])
        else:
            form = FormDonate()
            msg = "total_target is close"

    else:
        form = FormDonate()
        msg = ''
    context = {
        'project': project,
        'tag': tag,
        'image': image,
        'form': form,
        'msg': msg,
        'avrg_rate':avrg_rate,
        'comment':comment,
    }
    return render(request, 'projectfund/detail_project.html',context)

@login_required()
def cancleProject(request,id):
    project = Project.objects.get(id=id)
    account1 = User.objects.get(username=request.user)
    account = Account.objects.get(email=account1.email)
    min = int(project.total_target) * .25
    print(min)
    if project.creator_id == account.id and int(project.donations) < min:
        project.delete()
    else:
        messages.error(request,'you can;t delete yhis')
        return redirect('projectfund:detail_project', id=id)
    return redirect('account:view_projects',id=account.id)

def project_tag(request, id):
    arr = []
    project = Project.objects.get(id=id)
    tags = ProjectTag.objects.filter(project_name_tag=project)
    for tag in tags:
        print(tag.tag)
        the_tags = ProjectTag.objects.filter(tag=tag.tag)
        for the_tag in the_tags:
            projects = Project.objects.filter(title=the_tag)
            for project in projects:
                 image = ProjectImage.objects.filter(project_name=project)
                 arr.append(image)
    context = {'arr': arr}
    print(len(arr))
    return render(request, 'projectfund/projecttag.html',context)

def create_project(request,id):
    if request.method == 'POST':
        account = Account.objects.get(id=id)
        form = CreateProject(data=request.POST)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.creator = account
            acc.save()
            return HttpResponse("project is created")
    else:
        form = CreateProject()
    context = {'form': form}
    return render(request,'projectfund/create_project.html',context)


def create_project_image_tag(request, id):
    project = Project.objects.get(id=id)
    account = Account.objects.get(id=project.creator_id)
    print(request.user)
    print(account)
    if account.email == request.user.email:
        if request.method == 'POST':
            formimage = ImageProjectFrom(data=request.POST,files=request.FILES)
            formtag = ProjectTagForm(data=request.POST)
            if formimage.is_valid():
                img = formimage.save(commit=False)
                img.project_name = project
                img.save()
            if formtag.is_valid():
                img = formtag.save(commit=False)
                img.project_name_tag = project
                img.save()
        else:
            formimage = ImageProjectFrom()
            formtag = ProjectTagForm()
    else:
        return HttpResponse("nooooooooooooooooooooooooooooooooo")
    context = {
        'formimage': formimage,
        'formtag': formtag,
               }
    return render(request,'projectfund/project_image_tag.html',context)



def project(request,project_name_id):
    image = ProjectImage.objects.filter(project_name_id=project_name_id)
    print(image)
    return render(request, 'projectfund/images.html', {'images': image})


def allproject(request):
     allproject = Project.objects.all()
     return render(request, 'projectfund/allproject.html', {'allprojects': allproject})


def sameproject(request,category):
     arr=[]
     sameprojects = Project.objects.filter(category=category)
     for ti in sameprojects:
         image = ProjectImage.objects.filter(project_name_id=ti.id)
         arr.append(image)

     print(arr)
     return render(request, 'projectfund/allproject.html', {'images': arr,'sameproject': sameprojects})


def project_detail(request, id):

    post = get_object_or_404(Project, id=id)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.proj = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'comment.html', {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
def add_rate(request,id):
    postt = get_object_or_404(Project, id=id)
    rates = postt.rates.filter(active=True)
    new_ratee = None
    if request.method == 'POST':
        rate_form = form_rate(data=request.POST)
        if rate_form.is_valid():
            new_ratee = rate_form.save(commit=False)
            new_ratee.ratee = postt
            new_ratee.save()
    else:
        rate_form = form_rate()
    return render(request, 'rate.html', {'postt': postt,
                                            'rates': rates,
                                            'new_ratee': new_ratee,
                                            'rate_form': rate_form})

    # context = {}
    # context['form'] = form_rate()
    # return render( request, "rate.html", context)


def avrg(request):
        total=0
        countt = Rate.objects.all()
        print(countt)
        count_rate= countt.count()
        for i in countt:
            total = total + int(i.rating)
        print(total)
        avrg_rate = total / count_rate
        context = {'countt': count_rate,'avrg_rate': avrg_rate}
        return render(request, 'avreg.html', context)


# def avrg(request):
#      total=0
#      my_str = ''.join(''.join(tup) for tup in RATING_CHOICES)
#      total =total + int(my_str)
#      rate_count = Rate.objects.Count('rating')
#      avrg_rate = total/rate_cunt
#      return (avrg_rate)

def home(request):
    return render(request, 'projectfund/home.html', {})


def project_category(request,category):
    projects = Project.objects.filter(category=category)
    image = []
    print(category)
    for project in projects:
        img = ProjectImage.objects.filter(project_name=project)
        image.append(img[0])
    context = {
        'l_projects': projects,
        'image': image,
    }
    return render(request, 'projectfund/project_category.html', context)


def search(request):
    context = {}
    if request.method == 'GET':
        the_title = request.GET['search']
        the_tag = request.GET['search']
        image = []
        image2 = []
        projects = Project.objects.filter(title=the_title)
        for project in projects:
            img = ProjectImage.objects.filter(project_name=project)
            image.append(img)
        tag_projects = ProjectTag.objects.filter(tag=the_tag)
        arr = []
        for tag in tag_projects:
            img = Project.objects.get(id=tag.project_name_tag_id)
            arr.append(img)
        for project in arr:
            img = ProjectImage.objects.filter(project_name=project)[0:1]
            if img[0] in image2 :
                continue
            image2.append(img[0])
            print(img)
        context = {
            'l_projects':projects,
            'tag_projects':arr,
            'image': image,
            'image2': image2,
        }
    return render(request,'projectfund/search.html',context)

def cal_denitions(request,id):
    account1 = User.objects.get(username=request.user)
    account = Account.objects.get(email=account1.email)
    caldonitions = Donation.objects.filter(acc=account)
    total = 0
    for i in caldonitions:
        total += int(i.donation_account_project)
    print(total)
    messages.error(request, total)
    return redirect('projectfund:detail_project', id=id)
    # return redirect('account:view_projects', id=account.id)
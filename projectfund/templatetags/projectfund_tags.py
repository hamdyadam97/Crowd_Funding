from django import template
from projectfund.models import Project,ProjectImage,Rate



register = template.Library()


@register.inclusion_tag('projectfund/last_projects.html')
def last_projects():
    projects = Project.objects.all()[0:5]
    image = []
    for project in projects:
        img = ProjectImage.objects.get(project_name=project)
        image.append(img)
    context = {
        'l_projects': projects,
        'image': image,
    }
    return context




@register.inclusion_tag('projectfund/the_highest_five_rated.html')
def the_highest_five_rated():
    projectrate = Rate.objects.all().order_by('rating')[0:5]
    projects = []
    image = []
    for project in projectrate:
        img = Project.objects.get(id=project.ratee_id)
        projects.append(img)
    for project in projects:
        img = ProjectImage.objects.get(project_name=project)
        image.append(img)


    context = {
        'l_projects': projects,
        'image': image,
        'projectrate':projectrate
    }
    return context

@register.inclusion_tag('projectfund/featured_projects.html')
def featured_projects():
    projects = Project.objects.all().filter(is_admin=True).order_by('start_date')
    image = []
    for project in projects:
        img = ProjectImage.objects.get(project_name=project)
        image.append(img)


    context = {
        'l_projects': projects,
        'image': image,
    }
    return context

@register.inclusion_tag('projectfund/pro_cat.html')
def category_projects():
    arr = Project.objects.all()
    projects = []
    for cat in arr:
        if cat.category not in projects:
            projects.append(cat.category)
        else:
            continue

    context = {
        'l_projects': projects,
    }
    return context




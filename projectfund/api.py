from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from account.models import Account
from .models import Project,ProjectTag,ProjectImage,Comment,Rate
from .serializers import ApiProjectAll,ProjectTagApi,ProjectImageApi,CommentApi



@api_view(['GET'])
def projectapiall(request):
    projects = Project.objects.all()
    data = ApiProjectAll(projects, many=True)
    return Response(data.data, status=HTTP_201_CREATED)

@api_view(['GET'])
def detail_project_api(request,id):
    project = Project.objects.get(id=id)
    tag = ProjectTag.objects.filter(project_name_tag=project)
    image = ProjectImage.objects.filter(project_name=project)
    countt = Rate.objects.filter(ratee=project)
    comment = Comment.objects.filter(proj=project)
    count_rate = countt.count()
    total = 0
    for i in countt:
        total = total + int(i.rating)
    try:
        avrg_rate = total / count_rate
    except Exception:
        avrg_rate = 'no rate here'

    data = ApiProjectAll(project)
    data_tage = ProjectTagApi(tag, many=True)
    data_image = ProjectImageApi(image, many=True)
    data_comment = ProjectImageApi(image, many=True)
    date_rate = avrg_rate
    return Response({'projecttag':data_tage.data,'project':data.data,'image':data_image.data,
                     'commentd':data_comment.data,'rate':avrg_rate}, status=HTTP_201_CREATED)

@api_view(['POST'])
def createprojectapi(request):
    form = ApiProjectAll(request.data)
    user = User.objects.get(username=request.user)
    account = Account.objects.get(email=user.email)
    if request.data and len(request.data)==5:
        print(len(request.data))
        project = Project.objects.create(**request.data,creator=account)
        data = ApiProjectAll(project)
        return Response(data.data,status=HTTP_201_CREATED)
    else:
        return Response({"error":"not valid data"},status=HTTP_400_BAD_REQUEST)

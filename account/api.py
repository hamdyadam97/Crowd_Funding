from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Account, Profile
from .serializers import AccountLogin, ProfileApi, ProjectApi
from projectfund.models import Project


@api_view(['POST'])
def signinapi(request):
    log = AccountLogin(request.data)
    if 'email' in request.data and 'password' in request.data:
        print("asdasda")
        User = Account.objects.filter(email=request.data['email'], password=request.data['password'])
        if len(User) > 0 and User is not None:
            username = User[0].firstname + " " + User[0].lastname
            authuser = authenticate(username=username, password=request.data['password'])
            login(request, authuser)
            data = AccountLogin(User,many=True)
            return Response(data.data,status=HTTP_201_CREATED)
    else:
        return Response({'error':'invalid data'},status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logoutapi(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'nice': "logout data yes"}, status=HTTP_201_CREATED)
    return Response({'error': "can't logout data"}, status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addprofileapi(request):
    user = User.objects.get(username=request.user)
    account = Account.objects.get(email=user.email)
    form = ProfileApi(request.data)
    if 'birthdate' in request.data and 'facebook' in request.data and 'country' in request.data:
        trainee = Profile.objects.create(birthdate=request.data['birthdate'], facebook=request.data['facebook'], country=request.data['country'],
                                         name=account)
        data = ProfileApi(trainee,)
        return Response(data.data, status=HTTP_201_CREATED)
    else:
        return Response({'error':'data error'}, status=HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def projectapi(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        account = Account.objects.get(email=user.email)
        project = Project.objects.filter(creator=account)
        data = ProjectApi(project,many=True)
        return Response(data.data,status=HTTP_201_CREATED)
    else:
        return Response({'error': 'data error'}, status=HTTP_400_BAD_REQUEST)


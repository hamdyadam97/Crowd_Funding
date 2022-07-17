from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('signup', signup, name='signup'),
    path('verify/<str:token>', verify, name='verify'),
    path('login/', signin, name='signin'),
    path('logout', logout, name='logout'),
    path('updateuser/<id>', updateuser, name='updateuser'),
    path('addprofile/<id>', addprofile, name='addprofile'),
    path('verify/<str:token>',verify,name='verify'),
    path('home/<int:id>', deletepage,name='deletepage'),
    path('delete/<int:id>', deleteAccount),
    path('profile/<id>', profile, name='users-profile'),
    path('viewprojects/<id>', view_projects, name='view_projects'),

]
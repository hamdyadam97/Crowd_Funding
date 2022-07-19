from django.urls import path
from .views import *
from .api import *
app_name = 'account'

urlpatterns = [
    path('signup', signup, name='signup'),
    path('verify/<str:token>', verify, name='verify'),
    path('login/', signin, name='signin'),
    path('logout', logout, name='logout'),
    path('updateuser/<id>', updateuser, name='updateuser'),
    path('addprofile/<id>', addprofile, name='addprofile'),
    path('verify/<str:token>',verify,name='verify'),
    path('deleteacc/<int:id>', deletepage,name='deletepage'),
    path('delete/<int:id>', deleteAccount),
    path('profile/<id>', profile, name='users_profile'),
    path('viewprojects/<id>', view_projects, name='view_projects'),
    path('signinapi/', signinapi, name='signinapi'),
    path('logoutapi/',logoutapi, name='logoutapi'),
    path('addprofileapi/',addprofileapi, name='addprofileapi'),
    path('projectapi/',projectapi, name='projectapi'),
]
from django.urls import path

from .api import *
from .views import *

app_name = 'projectfund'

urlpatterns = [
    # path('projectapiall/',projectapiall, name='projectapiall'),
    path('', list_project, name='list_project'),
    path('detailproject/<id>', detail_project, name='detail_project'),
    path('projecttag/<id>', project_tag, name='project_tag'),
    path('createproject/<id>', create_project, name='create_project'),
    path('projectimagetag/<id>', create_project_image_tag, name='create_project_image_tag'),
    # path('projecttag/<tag>', project_tag, name='project_tag'),
    path('project/<int:project_name_id>', project),
    path('allproject/', allproject),
    path('allproject/<str:category>', sameproject,name='allproject'),
    path('comment/<id>',project_detail),
    path('rate/<id>',add_rate),
    path('avrg',avrg),
    path('allproject/<str:category>', sameproject),
    path('comment/<id>',project_detail,name='addcomment'),
    path('rate/<id>',add_rate,name='rateproject'),
    path('avrg',avrg,name='avrg'),
    path('home',home,name='home'),
    path('<str:category>',project_category,name='project_category'),
    path('search/',search, name='search'),
    path('cancel/<id>',cancleProject, name='cancel'),
    path('cal_denitions/<id>',cal_denitions, name='cal_denitions'),
    path('projectapiall/',projectapiall, name='projectapiall'),
    path('detail_project_api/<id>',detail_project_api, name='detail_project_api'),
    path('createprojectapi/',createprojectapi, name='createprojectapi'),
]


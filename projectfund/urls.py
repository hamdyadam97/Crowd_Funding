from django.urls import path
from .views import *

app_name = 'projectfund'

urlpatterns = [
    path('', list_project, name='list_project'),
    path('detailproject/<id>', detail_project, name='detail_project'),
    path('projecttag/<id>', project_tag, name='project_tag'),
    path('createproject/<id>', create_project, name='create_project'),
    path('projectimagetag/<id>', create_project_image_tag, name='create_project_image_tag'),
    # path('projecttag/<tag>', project_tag, name='project_tag'),
    path('project/<int:project_name_id>', project),
    path('allproject/', allproject),
    path('allproject/<str:category>', sameproject),
    path('comment/<id>',project_detail,name='addcomment'),
    path('rate/<id>',add_rate,name='rateproject'),
    path('avrg',avrg,name='avrg'),
    path('home',home,name='home'),
    path('<str:category>',project_category,name='project_category'),
    path('search/',search, name='search'),
    path('cancel/<id>',cancleProject, name='cancel'),
    path('cal_denitions/<id>',cal_denitions, name='cal_denitions'),
]


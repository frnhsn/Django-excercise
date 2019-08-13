from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from Boards import views as boards_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', boards_views.BoardsListView.as_view(), name='boards_list'),
    path('boards/<pk>', boards_views.TopicsListView.as_view(), name='topics_list'),
    path('boards/<pk>/topics/new', boards_views.NewTopic, name='new_topic'),
    path('boards/<pk>/topics/<slug>', boards_views.TopicView.as_view(), name='topic_view'), 
    path('boards/<pk>/topics/<slug>/new', boards_views.NewReply, name='new_reply'), 
    path('accounts/', include('django.contrib.auth.urls')),
]

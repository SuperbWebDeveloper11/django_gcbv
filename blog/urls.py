from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('post/', views.PostList.as_view(), name='post_list'),
    path('post/add/', views.PostCreate.as_view(), name='post_add'),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),

    # ************** post detail ************** 
    # create comment 
    path('post/<int:pk>/detail/', views.PostDetail.as_view(), name='post_detail'), 
    # update comment 
    path('post/<int:pk>/detail/<int:comment_pk>/update/', views.PostUpdateComment.as_view(), name='post_update_comment'), 
    # delete comment 
    path('post/<int:pk>/detail/<int:comment_pk>/delete/', views.PostDeleteComment.as_view(), name='post_delete_comment'), 
]

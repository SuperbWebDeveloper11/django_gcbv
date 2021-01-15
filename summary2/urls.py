from django.urls import path
from . import views

app_name = 'summary2'

urlpatterns = [
    # summary urls for crud operations
    path('summary/', views.SummaryList.as_view(), name='summary_list'),
    path('summary/add/', views.SummaryCreate.as_view(), name='summary_add'),
    path('summary/<int:pk>/detail/', views.SummaryDetail.as_view(), name='summary_detail'),
    path('summary/<int:pk>/detail2/', views.SummaryDetail2.as_view(), name='summary_detail2'),
    path('summary/<int:pk>/update/', views.SummaryUpdate.as_view(), name='summary_update'),
    path('summary/<int:pk>/delete/', views.SummaryDelete.as_view(), name='summary_delete'),

]

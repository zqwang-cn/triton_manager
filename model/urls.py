from django.urls import path
from . import views

urlpatterns = [
    path('', views.ModelList.as_view()),
    path('<str:pk>/', views.ModelDetail.as_view()),
    path('<str:name>/versions/', views.VersionList.as_view()),
    path('<str:name>/versions/<int:version>/', views.VersionDetail.as_view()),
]
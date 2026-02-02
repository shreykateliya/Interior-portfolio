from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/', views.portfolio_list, name='portfolio'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about, name='about'),
]


from django.urls import path
from . import views
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('administration/', views.admin_view, name='administration'),
    path('ajout-equipment/', views.ajout_equipment_view, name='ajout_equipment'),
    path('charts/', views.charts_view, name='charts'),
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('membre/', views.membre_view, name='membre'),
    path('password/', CustomPasswordResetView.as_view(), name='password'),
    path('register/', views.register_view, name='register'),
    path('tables/', views.tables_view, name='tables'),
    path('500/', views.error_500_view, name='500'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('logout/', views.CustomLogoutView, name='logout'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('delete_equipement/<int:id>/', views.delete_equipment, name='delete_equipment'),
    path('get_equipement/<int:id>/', views.get_equipement, name='get_equipement'),
    path('ajout_equipment/<int:id>/', views.ajout_equipment_view, name='edit_equipement'), 
       path('ajout_utilisateur/', views.ajout_utilisateur_view, name='ajout_utilisateur'),
        path('delete_membre/<int:id>/', views.delete_membre, name='delete_membre'),
         path('get_utilisateur/<int:id>/', views.get_utilisateur, name='get_utilisateur'),
          path('ajout_utilisateur/<int:id>/', views.ajout_utilisateur_view, name='edit_utilisateur'), 
          path('ajout_admin/', views.ajout_admin_view, name='ajout_admin'),
             path('ajout_admin/<int:id>/', views.ajout_admin_view, name='edit_admin'), 
               path('delete_admin/<int:id>/', views.delete_admin, name='delete_admin'),
         path('get_admin/<int:id>/', views.get_admin, name='get_admin'),
]

from django.urls import path
from . import views  

urlpatterns = [
    path('registration', views.user_registration, name='registration'),
    path('login', views.login, name='login'),
    # path('create_project/', views.create_project, name='create_project'),
    # path('assign_projects/', views.assign_projects, name='assign_projects'),

    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/block/', views.block_project, name='block_project'),
    path('projects/<int:project_id>/unblock/', views.unblock_project, name='unblock_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('projects/<int:project_id>/assign/', views.assign_projects, name='assign_project'),

    path('create_ticket/<int:project_id>', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('assigned-tickets/', views.assigned_tickets, name='assigned_tickets'),
    path('ticket/<int:ticket_id>/update/', views.update_ticket_status, name='update_ticket_status'),
    path('ticket/<int:ticket_id>/check/', views.check_ticket, name='check_ticket'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('profile/', views.update_profile, name='profile'),

    path('logout/', views.logout_view, name='logout'),
]   

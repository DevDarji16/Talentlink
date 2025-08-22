from django.urls import path
from .views import check_user,check_username,create_profile,get_profile,check_login,gigs_view,jobs_view,update_profile,add_project,get_all_freelancers,get_freelancer_by_username,edit_project,delete_project,get_gig_by_id,get_job_by_id,get_person_by_username,FreelanceGroupDetailView,create_group,my_groups,joined_groups,get_groups,search_users,send_group_invite,respond_group_invite,mark_notification_read,get_notifications,create_application,respond_to_application,list_job_applications
from .views import disable_gig,edit_gig,enable_gig,remove_member_from_group,update_group_details
urlpatterns=[

    path('check_user/',check_user),
    path('check_username/',check_username),
    path('create_profile/',create_profile),
    path('get_profile/',get_profile),
    path('check_login/',check_login),
    path('jobs/', jobs_view),
    path('update_profile/',update_profile),
    path('get_all_freelancers/',get_all_freelancers),
    path('freelancer/<str:username>/', get_person_by_username),
    path('client/<str:username>/', get_person_by_username),
    path('add_project/', add_project),
    path('edit_project/', edit_project),
    path('delete_project/', delete_project),
    
    path('gigs/', gigs_view),
    path('gig/<int:id>', get_gig_by_id),
    path('gigs/<int:gig_id>/disable/', disable_gig, name='disable-gig'),
    path('gigs/<int:gig_id>/enable/', enable_gig, name='disable-gig'),
    path('gigs/<int:gig_id>/edit/', edit_gig, name='edit-gig'),
    
    path('job/<int:id>', get_job_by_id),



    path('group/<int:pk>/',FreelanceGroupDetailView.as_view(),name='group-detail'),
    path('group/create/',create_group,name='create_group'),
    path('group/my_groups/',my_groups,name='my_groups'),
    path('group/joined_groups/',joined_groups,name='joined_groups'),
    path('groups/',get_groups,name='get_groups'),
    path('group/<int:group_id>/remove_member/', remove_member_from_group, name='remove_member'),
    path('group/<int:group_id>/update/', update_group_details, name='update_group'),

    path('search/',search_users,name='search_users'),

    path('group/<int:group_id>/invite',send_group_invite),
    path('group/<int:invite_id>/respond',respond_group_invite),
    path('mark_notification_read/<int:pk>/',mark_notification_read),
    path('notifications/',get_notifications),

    path('applications/', create_application),
    path('jobs/<int:job_id>/applications/', list_job_applications),
    path('applications/<int:application_id>/respond/', respond_to_application),

   
]

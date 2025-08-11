from django.urls import path
from .views import check_user,check_username,create_profile,get_profile,check_login,gigs_view,jobs_view,update_profile,add_project,get_all_freelancers,get_freelancer_by_username,edit_project,delete_project,get_gig_by_id,get_job_by_id,apply_to_job,get_person_by_username,FreelanceGroupDetailView,create_group,my_groups,joined_groups,get_groups

urlpatterns=[

    path('check_user/',check_user),
    path('check_username/',check_username),
    path('create_profile/',create_profile),
    path('get_profile/',get_profile),
    path('check_login/',check_login),
    path('gigs/', gigs_view),
    path('jobs/', jobs_view),
    path('update_profile/',update_profile),
    path('get_all_freelancers/',get_all_freelancers),
    path('freelancer/<str:username>/', get_person_by_username),
    path('client/<str:username>/', get_person_by_username),
    path('add_project/', add_project),
    path('edit_project/', edit_project),
    path('delete_project/', delete_project),
    path('gig/<int:id>', get_gig_by_id),
    path('job/<int:id>', get_job_by_id),
    path('job/<int:job_id>/apply/', apply_to_job, name='apply-to-job'),
    path('group/<int:pk>/',FreelanceGroupDetailView.as_view(),name='group-detail'),
    path('group/create/',create_group,name='create_group'),
    path('group/my_groups/',my_groups,name='my_groups'),
    path('group/joined_groups/',joined_groups,name='joined_groups'),
    path('groups/',get_groups,name='get_groups'),
    # path('groups/create/', create_group),
    # path('freelancers/search/<str:username>/', search_freelancers),

]

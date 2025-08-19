from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_draft, name="create-draft"),
    path("mine/", views.my_drafts, name="my-drafts"),  # drafts created by me (freelancer)
    path("for-me/", views.drafts_for_client, name="drafts-for-client"),  # drafts I received (as client)
    path("<int:draft_id>/respond/", views.respond_to_draft, name="respond-to-draft"),
    path("search-clients/", views.search_clients, name="search-clients"),
    path("<int:draft_id>/", views.draft_detail, name="draft-detail"),

]

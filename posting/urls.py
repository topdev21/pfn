from django.urls import path, include
from .views import HomePage, CourseDetail, LevelDetail,get_next_level_data, NewLetterPost, createPost, display, CourseUpdate, Profile, replay
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("",HomePage.as_view(), name="homepage"),
    path('python-course/<slug:slug>', display.as_view(), name="coursedetail"),
     path('python-course/<slug:slug>/edit', CourseUpdate.as_view(), name="update"),
    path('python-course-level/<slug:slug>', LevelDetail.as_view(), name="niveaudetail"),
    path("newletters", csrf_exempt(NewLetterPost.as_view()), name="newletter"),
    path("make-new-course",createPost.as_view(), name="create" ),
    path("accounts/profile",Profile.as_view(), name="profile" ),

    path("replay/<int:pk>/",replay.as_view(), name="replayToComment"),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path("python-course-level/next-level/<slug:slug>-<int:initial>/",get_next_level_data.as_view(), name="page_level")
]
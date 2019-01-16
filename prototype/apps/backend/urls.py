
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from .views import *

# Create a router and register our viewsets with it.

router = DefaultRouter()
#router.register(r'admins', AdminViewSet)
router.register(r'candidates', CandidateViewSet)
router.register(r'candidate-skills', CandidateSkillViewSet)
router.register(r'candidate-docs', DocumentViewSet)
router.register(r'employers', EmployerViewSet)
router.register(r'recruiters', RecruiterViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'job-posts', JobPostViewSet)
router.register(r'job-posts-and-skills', JobPostAndSkillsViewSet)
router.register(r'job-skills', JobSkillViewSet)
router.register(r'job-matches', JobMatchViewSet)
router.register(r'job-matches-and-posts', JobMatchAndPostViewSet)
router.register(r'job-matches-and-candidates', JobMatchAndCandidateViewSet)
router.register(r'favourites-candidates', FavouritesCandidatesViewSet)
router.register(r'favourites-jobs', FavouritesJobsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^upload-doc/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    url(r'^photo-upload/(?P<filename>[^/]+)$', PhotoUploadView.as_view()),
    url(r'^download/(?P<user>[^/]+)/(?P<filename>[^/]+)$', FileDownloadView.as_view()),
    url(r'^files/(?P<user>[^/]+)/$', FileListView.as_view()),
    url(r'^create-matches/$', AutoMatchView.as_view()),
    url(r'^create-manual-match/$', ManualMatchView.as_view())
]

from .views import FileViewSet, SnippetViewSet, SnippetPreviewViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

app_name = 'snippets'

router = DefaultRouter()
router.register('previews', SnippetPreviewViewSet, basename='preview')
router.register('', SnippetViewSet, basename='snippet')
router.register(r'(?P<snippet_id>\d+)/comments', CommentViewSet, basename='snippet-comments')
router.register(r'(?P<snippet_id>\d+)/files', FileViewSet, basename='snippet-files')

urlpatterns = router.urls

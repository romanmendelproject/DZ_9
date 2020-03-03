from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from .views import CourseViewSet, LessonViewSet, StudentViewSet, TeacherViewSet

router = DefaultRouter()
router.register('teacher', TeacherViewSet)
router.register('student', StudentViewSet)
router.register('course', CourseViewSet)
router.register('lesson', LessonViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

# yourapp/urls.py
from django.urls import path
from .views import (
       ConfirmRegistrationView, RegisterEmailView, CourseRegisterView, 
       EditCourseView,EditPostView,EditEventView,
        PostRegisterView, ResetPasswordView, 
        StudentCourseDetailView, RegisterSalesView,
        RetrieveSalesView,
         VideoRegisterView,
        BooksRegisterView, CourseFilter,
        StudentEventView, stk_push, CouponRegisterView
)

from . import views 
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('account/create/', views.RegisterStaffView.as_view(), name='staff_auth_register'),
    path('api/register/staff', views.RegisterStaffView.as_view(), name='register-staff'),
    path('api/register/student', views.RegisterStudentView.as_view(), name='register-student'),
    path('api/register/sales', views.RegisterSalesView.as_view(), name='register-student'),
    path('api/register/books', views.BooksRegisterView.as_view(), name='register-books'),
    path('api/register/book/<str:pk>/', views.BooksRegisterView.as_view(), name='register-books'),
    path('api/register/video/', views.VideoRegisterView.as_view(), name='video-register'),
    path('api/access/videos/<str:pk>/', views.VideoRegisterView.as_view(), name='video-register'),
    
    path('api/register/coupon', views.CouponRegisterView.as_view(), name='coupon-register'),
    path('api/register/coupon/<str:pk>/', views.CouponRegisterView.as_view(), name='coupon-register'),

    path('api/register/coupon-course', views.CouponPurchaseListCreateAPIView.as_view(), name='coupon-register'),
    path('api/register/coupon-course/<str:pk>/', views.CouponPurchaseRetrieveUpdateDestroyAPIView.as_view(), name='coupon-register'),
    
    path('api/user/student/', views.StudentUserView.as_view(), name='register'),
    path('confirm-registration/<str:uidb64>/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm-registration'),

    path('api/user/staff/', views.StaffUserView.as_view(), name='register'),
    path('api/user/sales/', views.SalesUserView.as_view(), name='register'),
    path('api/course/filter/', views.CourseFilter.as_view(), name='register'),
    path('api/user/update/<str:pk>/', views.UpdateStudentView.as_view(), name='register'),
    path('api/register/email',  RegisterEmailView.as_view(), name='email-register'),
    path('api/register/course',  CourseRegisterView.as_view(), name='course-register'),
    path('api/edit/course/<int:pk>/', EditCourseView.as_view(), name='edit-course-register'),
    path('api/student/event/<int:pk>/', StudentEventView.as_view(), name="student-event-view"),
    path('api/student/sales/<int:pk>/', RetrieveSalesView.as_view(), name="student-event-view"),


    path('api/edit/post/<int:pk>/', EditPostView.as_view(), name='edit-course-register'),
    path('api/edit/event/<int:pk>/', EditEventView.as_view(), name='edit-course-register'),
    path('api/students/course/<int:user_id>/<int:course_id>/', views.BuyCourseView.as_view(), name='buy-course'),
    path('api/students/courses/<int:pk>/', views.BuyCourseView.as_view(), name='buy-course'),
    path('api/retrieve/course/<str:pk>/', StudentCourseDetailView.as_view(), name='course-register'),
    path('api/register/post', PostRegisterView.as_view(), name='post-register'),
    path('api/register/events/', views.EventListView.as_view(), name='event-list'),
    path('api/register/event/<str:pk>/', views.EventListView.as_view(), name='event-list'),
    path('api/register/events/<str:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('api/students/profile/<int:pk>/', views.StudentProfileDetailView.as_view(), name='event-detail'),
    path('api/stk-push/', views.stk_push.as_view(), name='stk_push'),

    # other urlpatterns...
]

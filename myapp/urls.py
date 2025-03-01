from django.urls import path
from .views import ProductListView, StudentListView
from .views import RequestOTPAPIView, VerifyOTPAPIView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:student_id>/', StudentListView.as_view(), name='student-detail'),  
    path('request-otp/', RequestOTPAPIView.as_view(), name='request-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),

]

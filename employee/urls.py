from django.urls import path
from rest_framework import routers

from employee.views import EmployeeList, EmployeeDetail

urlpatterns = [
    path('employee/', EmployeeList.as_view()),
    path('employee/<int:pk>/', EmployeeDetail.as_view()),
]

router = routers.DefaultRouter()
urlpatterns += router.urls

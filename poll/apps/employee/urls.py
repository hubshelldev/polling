from django.urls import path

from apps.employee import views

app_name = 'employee'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('usercreate/',views.Employee.as_view(),name="create_user"),
    path('employeelist/',views.EmployeeViewList.as_view(),name="employee_list")
    ]
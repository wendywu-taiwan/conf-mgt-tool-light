from django.urls import path

from permission import views
from django.conf.urls import url, include

app_name = 'permission'

permission_pattern = [
    path('', views.permission_index_page, name="permission-index"),

]

user_role_pattern = [
    path('user_role', views.setting_user_role_list_page, name="user-role-list"),
    path('user_role/edit', views.setting_user_role_edit_page, name="user-role-list"),
]

urlpatterns = [
    path('admin_console/permission/', include(user_role_pattern)),
    path('admin_console/permission/', include(permission_pattern)),
]

from django.urls import path

from permission import views
from django.conf.urls import url, include

app_name = 'permission'

permission_pattern = [
    path('', views.permission_index_page, name="permission-index"),

]

user_role_pattern = [
    path('user_role', views.setting_user_role_list_page, name="user-role-list-page"),
    path('user_role/edit', views.edit_user_role, name="user-role-edit"),
    path('user_role/edit/<str:user_id>', views.setting_user_role_edit_page, name="user-role-edit-page"),
]

urlpatterns = [
    path('admin_console/permission/', include(user_role_pattern)),
    path('admin_console/permission/', include(permission_pattern)),
]

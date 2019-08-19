from django.urls import path

from permission import views
from django.conf.urls import include

app_name = 'permission'

permission_pattern = [
    path('', views.permission_index_page, name="permission-index"),

]

user_role_pattern = [
    path('user_role', views.setting_user_role_list_page, name="user-role-list-page"),
    path('user_role/edit', views.edit_user_role, name="user-role-edit"),
    path('user_role/edit/<str:user_id>', views.setting_user_role_edit_page, name="user-role-edit-page"),
]

role_permission_pattern = [
    path('role', views.setting_role_permission_list_page, name="role-permission-list-page"),
    path('role/edit/<str:environment_id>', views.setting_role_permission_edit_page, name="role-permission-edit-page"),
    path('role/edit', views.edit_role_permission, name="role-permission-edit"),
]

urlpatterns = [
    path('admin_console/permission/', include(permission_pattern)),
    path('admin_console/permission/', include(role_permission_pattern)),
    path('admin_console/permission/', include(user_role_pattern)),
]

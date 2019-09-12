from django.urls import path

from permission import views
from django.conf.urls import include

app_name = 'shared_storage'

ftp_pattern = [
    path('diff', views.permission_index_page, name="permission-index"),

]

urlpatterns = [
    path('shared_storage/', include(ftp_pattern)),
]

from django.urls import path
from . import views
urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('login/forgot_password', views.forgot_password, name='forgot_password'),
    path('login/password_reset', views.password_reset, name='password_reset'),
    path('logout', views.logout_view, name='logout'),
    path('homepage', views.homepage, name='homepage'),
    path('homepage/tuitionpackage', views.tuitionpackage, name="tuitionpackage"),
    path('homepage/registration', views.registration, name='registration'),
    path('homepage/registration/update_registration/<str:id>', views.update_registration, name='update_registration'),
    path('homepage/registration/save_update_registration/<str:id>', views.save_update_registration, name='save_update_registration'),
    path('homepage/registration/clear_registration', views.clear_registration, name='clear_registration'),
    path('homepage/suggestion', views.suggestion, name='suggestion'),
    path('homepage/suggestion/new_suggestion', views.new_suggestion, name='new_suggestion'),
    path('homepage/suggestion/delete_suggestion/<int:suggestion_id>/', views.delete_suggestion, name='delete_suggestion'),
    path('homepage/my_account', views.my_account, name='my_account'),
    path('homepage/update_my_account', views.update_my_account, name='update_my_account'),
]

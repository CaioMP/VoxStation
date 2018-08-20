from django.urls import path
from django.contrib.auth.decorators import login_required
from account import views


app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView, name='sign_in'),
    path('logout/', login_required(views.logout_view), name='sign_out'),
    path('signup/', views.RegisterView, name='sign_up'),
    path('profile/edit/', login_required(views.edit_profile), name='edit_profile'),
    path("following/<int:cod>/", views.following, name='following'),
    path("historic/<int:cod>/", views.historic, name='historic'),
    path("new_channel/", login_required(views.NewChannelView), name='new_channel'),
    path("myPlaylist/<int:cod>/", views.myPlaylists, name='myplaylists'),
    path("change_password/", login_required(views.change_password), name='change_password')

]

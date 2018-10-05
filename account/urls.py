from django.urls import path
from django.contrib.auth.decorators import login_required
from account.views import *


app_name = 'account'

urlpatterns = [
    path('login/', LoginView, name='sign_in'),
    path('logout/', login_required(logout_view), name='sign_out'),
    path('signup/', RegisterView, name='sign_up'),
    path('profile/edit/', login_required(edit_profile), name='edit_profile'),
    path("historic/", historic, name='historic'),
    path("favorites/", favorites, name='favorites'),
    path("new_channel/", login_required(NewChannelView), name='new_channel'),
    path("change_password/", login_required(change_password), name='change_password'),
    path("removeHistoric/<int:idAudio>", login_required(RemoveHistoric), name='remove_historic_view'),
    path("removeFavorites/<int:idAudio>", login_required(RemoveFavorites), name='remove_fav'),
    path("notific/<int:canal_id>", login_required(notific), name='notific_view')
]

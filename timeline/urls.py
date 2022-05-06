from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('comments/<int:post_pk>', views.comments, name="comments"),
    path('user/<int:user_pk>', views.public_profile, name="public_profile"),
    path('post/<int:post_pk>', views.post_edit, name="edit_post"),
    path('like', views.like_post, name='like'),
    path('dislike', views.dislike_post, name='dislike')
    # path('like/<int:post_pk>', views.likebtn,name="liking"),
    # path('dislike/<int:post_pk>', views.dislikebtn,name="disliking"),


]

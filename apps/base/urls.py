from django.urls import path
from . import views
from apps.authentication.views import user_profile
from apps.notfound import notFound404

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("profile/<int:user_id>/", user_profile, name="profile"),
    path("send-friend-request/<int:receiver_id>/",
         views.SendFriendRequestView.as_view(), name='friend_request'),
    path("friends/requests/", views.FriendRequestView.as_view(),
         name='friend_requests'),
    path('friends/', views.AllFriendsView.as_view(), name='friends'),
    path("friends/all/", views.FriendsView.as_view(), name='all_friends'),
    path("profile/friend/<int:user_id>/",
         views.ProfileFromFriendSection.as_view(), name="profile_friends"),
    path("remove/friend/<int:receiver_id>/",
         views.RemoveFriendRequestView.as_view(), name='friend_delete'),
    path("post/<int:postID>/", views.post_detail, name='post_detail'),
    path("404/", notFound404, name="404_notfound"),
    
    
    # phone
    path('p/post/', views.mobile_post, name='mobile_post')
    
]
# monkeytype.com

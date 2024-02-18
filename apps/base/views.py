from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from apps.authentication.models import User, FriendRequest, Friendship
from django.views.generic import RedirectView, ListView
from django.core import serializers
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.utils import timezone
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

import json

from .models import File, Post, Comment, Like
from apps.story.models import Story


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "home/home.html"
    login_url = "/"

    def custom_search(self):
        if self.request.method == "GET":
            search = self.request.GET.get("user_search")
            return search

    def get_file_type(self, file):
        # Check file type based on file extension or other criteria
        if (
            file.name.endswith(".jpg")
            or file.name.endswith(".jpeg")
            or file.name.endswith(".png")
        ):
            return "image"
        elif (
            file.name.endswith(".mp4")
            or file.name.endswith(".avi")
            or file.name.endswith(".mov")
        ):
            return "video"
        else:
            return "unknown"

    def post(self, request):
        if self.request.method == "POST":
            postID = self.request.POST.get("data-post-id")
            like = request.POST.get("post__like")
            likePostID = request.POST.get("post__like-postID")
            if postID:
                post = Post.objects.get(id=postID)
                post.is_hidden = True
                post.hide_from = self.request.user
                post.save()
            if like and likePostID:
                getPostForLike = Post.objects.get(id=likePostID)
                liked = Like.objects.filter(
                    user=request.user, post=getPostForLike).exists()
                if not liked:
                    Like.objects.create(user=request.user,
                                        post=getPostForLike, like=True)
                else:
                    lk = Like.objects.get(
                        user=request.user, post=getPostForLike)
                    lk.delete()

            content = self.request.POST.get("post_message")
            file = self.request.FILES.get("file_post")
            if file and content:
                chosen_file = File.objects.create(file=file)
                chosen_post = Post.objects.create(
                    user=self.request.user, content=content
                )
                chosen_post.content_type = ContentType.objects.get_for_model(
                    chosen_file
                )
                chosen_post.object_id = chosen_file.id
                chosen_post.save()
            if content and not file:
                chosen_post = Post.objects.create(
                    user=self.request.user, content=content
                )
                chosen_post.save()
            if file and not content:
                chosen_file = File.objects.create(file=file)
                chosen_post = Post.objects.create(user=self.request.user)
                chosen_post.content_type = ContentType.objects.get_for_model(
                    chosen_file
                )
                chosen_post.object_id = chosen_file.id
                chosen_post.save()

        return redirect("/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        custom_search = self.custom_search()
        current_user = self.request.user
        search_me = False
        friend_send_status = False
        if custom_search:
            users = User.objects.filter(
                Q(firstname__icontains=custom_search)
                | Q(lastname__icontains=custom_search)
            ).exclude(Q(is_admin=True) | Q(email=current_user.email))
            current = User.objects.filter(
                Q(firstname__icontains=custom_search)
                | Q(lastname__icontains=custom_search)
            )
            for x in current:
                if x.firstname == current_user.firstname:
                    search_me = True

                if x.lastname == current_user.lastname:
                    search_me = True
                if x.firstname == current_user.lastname:
                    search_me = True
                if x.lastname == current_user.firstname:
                    search_me = True

            friend_send_statuses = []

            for user in users:
                """
                friend_send_status ---> do'stlik so'rovni tekshiradi
                current_user ---> joriy user
                """
                friend_send_status = (
                    user.friend_send_status
                ) = current_user.friend_send_status(user)
                friend_send_statuses.append(friend_send_status)

            context["search_me"] = search_me
            context["users"] = zip(users, friend_send_statuses)
            context["found"] = users
            context["friend_send_status"] = friend_send_status
            context["custom_search"] = self.custom_search()

        trues = []
        hide_posts = []
        posts = Post.objects.all()

        for x in posts:
            if not x.hide_from == self.request.user:
                hide_posts.append(False)
            elif x.hide_from == self.request.user:
                hide_posts.append(True)

        for x in posts:
            if x.content_object:
                if x.content_object.file.name[-3:] == "mp4":
                    trues.append(True)
                else:
                    trues.append(False)
            else:
                trues.append(False)

        comment_count_list = []
        like_count_list = []
        is_like = []
        for post in posts:
            context["comment_count"] = Comment.objects.all().filter(
                post=post).count()
            likes = Like.objects.all().filter(post=post, user=self.request.user)
            if not likes:
                is_like.append(False)
            if likes:
                for like in likes:
                    if not like.user == self.request.user:
                        is_like.append(False)
                    else:
                        is_like.append(True)
            context['is_like'] = is_like
            context["likes_person_two"] = Like.objects.filter(post=post)[:2]
            like_count = Like.objects.all().filter(post=post).count()
            if like_count > 2:
                like_count -= 2
            if like_count:
                like_count_list.append(like_count)
            if not like_count:
                like_count_list.append(0)
            context["like_count"] = like_count
            comment_count = Comment.objects.all().filter(post=post).count()
            if comment_count:
                comment_count_list.append(comment_count)
            else:
                comment_count_list.append(0)

            comment_k = False
            if comment_count > 1000 and comment_count < 1000000:
                comment_k = True
            context['comment_k'] = comment_k

        is_our_stories = []
        stories = Story.objects.all()

        context['comment_count_list'] = comment_count_list
        context['like_count_list'] = like_count_list
        for story in stories:
            if story.user == self.request.user:
                is_our_stories.append(True)
            else:
                is_our_stories.append(False)
        context['stories'] = zip(Story.objects.all(), is_our_stories)

        if is_like and comment_count_list:
            context["videos"] = zip(
                posts, trues, hide_posts, is_like, comment_count_list, like_count_list)
        elif is_like:
            context["videos"] = zip(
                posts, trues, hide_posts, is_like, like_count_list, like_count_list)
        elif comment_count_list:
            context["videos"] = zip(
                posts, trues, hide_posts, comment_count_list, like_count_list)
        else:
            context["videos"] = zip(posts, trues, hide_posts, like_count_list)
        return context


class SendFriendRequestView(LoginRequiredMixin, RedirectView):
    pattern_name = "home"

    def get_redirect_url(self, *args, **kwargs):
        # qabul qiluvchini idsni olish
        receiver_id = self.kwargs.get("receiver_id")
        requester = self.request.user

        # So'rov yuborilayotgan do'stimiz bizda do'stlar qatorida bormi yoki yoq(tekshirish)
        if (
            not FriendRequest.objects.filter(
                requester=requester, receiver_id=receiver_id
            ).exists()
            and not Friendship.objects.filter(
                Q(user1=requester)
                | Q(user2_id=receiver_id)
                | Q(user1_id=receiver_id)
                | Q(user2=requester)
            ).exists()
        ):
            # Agar bo'lmasa Do'st so'rovini yaratish kerak
            FriendRequest.objects.create(
                requester=requester, receiver_id=receiver_id)

        return reverse(self.pattern_name)


class FriendRequestView(TemplateView):
    template_name = "home/friend_requests.html"


class AllFriendsView(LoginRequiredMixin, ListView):
    model = FriendRequest
    context_object_name = "friends_requests_received"
    template_name = "home/all_friends.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(
            receiver=self.request.user, status=FriendRequest.PENDING
        )
        return queryset

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        have_request = False
        if self.get_queryset():
            have_request = True

        contex["have_request"] = have_request
        return contex

    def post(self, request, *args, **kwargs):
        request_id = self.request.POST.get("request_id")
        action = self.request.POST.get("action")

        if request_id and action:
            self.handle_friendship(int(request_id), action)
        return redirect("home")

    def handle_friendship(self, request_id, action):
        friend_request = FriendRequest.objects.get(id=request_id)
        if action == "accept":
            friend_request.status = FriendRequest.ACCEPTED

            Friendship.objects.create(
                user1=friend_request.requester, user2=friend_request.receiver
            )

        elif action == "decline":
            friend_request.status = FriendRequest.DECLINED

        friend_request.delete()
        return redirect("home")


class FriendsView(LoginRequiredMixin, ListView):
    model = Friendship
    context_object_name = "friends"
    template_name = "home/friends_section.html"

    def get_queryset(self):
        user = self.request.user
        queryset = self.model.objects.filter(Q(user1=user) | Q(user2=user))

        return queryset

    def get_context_data(
        self,
        **kwargs,
    ):
        context = super().get_context_data(**kwargs)
        # barcha do'stlar sonini olish uchun
        context["friend_count"] = Friendship.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        ).count()
        return context


class RemoveFriendRequestView(LoginRequiredMixin, RedirectView):
    pattern_name = "all_friends"

    def get_redirect_url(self, *args, **kwargs):
        # qabul qiluvchini idsni olish
        user1 = self.request.user
        user2 = self.kwargs.get("receiver_id")

        if Friendship.objects.filter(user1=user1, user2=user2):
            friend = Friendship.objects.get(user1=user1, user2=user2)
            messages.warning(
                self.request,
                "Siz {} {} ni do'stlar qatoridan o'chirib yubordingiz".format(
                    friend.user2.firstname, friend.user2.lastname
                ),
            )
            friend.delete()

        elif Friendship.objects.filter(user1=user2, user2=user1):
            friend = Friendship.objects.get(user1=user2, user2=user1)
            messages.warning(
                self.request,
                "Siz {} {} ni do'stlar qatoridan o'chirib yubordingiz".format(
                    friend.user1.firstname, friend.user1.lastname
                ),
            )
            friend.delete()

        return reverse(self.pattern_name)


class ProfileFromFriendSection(LoginRequiredMixin, ListView):
    model = Friendship
    context_object_name = "friends"
    template_name = "home/profile_friends.html"

    def get_queryset(self):
        user = self.request.user
        queryset = self.model.objects.filter(Q(user1=user) | Q(user2=user)).exclude(
            Q(user1=user) & Q(user2=user)
        )
        return queryset

    def get_context_data(
        self,
        **kwargs,
    ):
        context = super().get_context_data(**kwargs)
        # barcha do'stlar sonini olish uchun
        context["friend_count"] = Friendship.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        ).count()
        context["user"] = User.objects.get(
            unique_id=self.kwargs.get("user_id"))
        return context


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def post_detail(request, postID):
    post = Post.objects.get(id=postID)
    if request.method == "POST" or is_ajax(request=request):
        text = request.POST.get("comment__post")
        like = request.POST.get("post_id")
        likes = Like.objects.filter(post=post)
        liked = Like.objects.filter(user=request.user, post=post).exists()
        is_like = False

        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
        if like:
            if not liked:
                Like.objects.create(user=request.user, post=post, like=True)
            else:
                lk = Like.objects.get(user=request.user, post=post)
                lk.delete()

        for like in likes:
            if like.user == request.user:
                is_like = True

        like_count = likes.count()  # get the count of likes
        like_count -= 2
        liked_users = [{"firstname": like.user.firstname,
                        "lastname": like.user.lastname} for like in likes]
        likes_person_two = liked_users[:2]

        comments = Comment.objects.filter(post=post).values(
            "text", "user__firstname", "date_commented", "user__lastname", "post", "user__profile__avatar")
        comment_count = comments.count()

        # Initialize lists for times and time_day
        times = []
        time_day = []
        # Calculate times and time_day
        for comment in comments:
            # Assuming timezone.now() is aware datetime
            diff_day = (timezone.now().date() -
                        comment['date_commented'].date()).days
            if diff_day == 0:
                times.append(abs(timezone.now().hour -
                             comment['date_commented'].hour))
                time_day.append(False)
            else:
                times.append(diff_day)
                time_day.append(True)

        comment_k = 1000 < comment_count < 1000000
        comment_m = comment_count > 1000000

        # Serialize comments
        serialized_comments = json.dumps(list(comments), cls=DjangoJSONEncoder)
        serialized_comments_loads = json.loads(serialized_comments)
        # Construct comments_data
        comments_data = [
            {
                "comment": comment['text'],
                "comment_firstname": comment['user__firstname'],
                "comment_lastname": comment['user__lastname'],
                "comment_avatar": comment['user__profile__avatar'],
                "times": times[i],
                "time_day": time_day[i],
            }
            for i, comment in enumerate(serialized_comments_loads)
        ]

        response_data = {
            "like_count": like_count,
            "likes_person_two": likes_person_two,
            "is_like": is_like,
            "comments": comments_data,
            "comment_count": comment_count,
            "comment_m": comment_m,
            "comment_k": comment_k
        }

        return JsonResponse(response_data, safe=False)
    if request.method == 'GET' or is_ajax(request=request):
        is_video = False
        is_text = False
        is_like = False
        if post.content_object:
            if post.content_object.file.name[-3:] == "mp4":
                is_video = True
            else:
                is_video = False
        else:
            is_text = True

        comments = Comment.objects.all().filter(post=post)

        likes = Like.objects.all().filter(post=post)

        for like in likes:
            if like.user == request.user:
                is_like = True

        likes_person_two = Like.objects.filter(post=post)[:2]
        like_count = Like.objects.all().filter(post=post).count()
        if like_count > 2:
            like_count -= 2

        times = []
        time_day = []
        comment_k = False  # ming
        comment_m = False  # mln
        for comment in comments:
            hour = comment.date_commented.hour
            minute = comment.date_commented.minute
            day = comment.date_commented.day
            diff = hour - timezone.now().hour
            diff_day = day - timezone.now().day
            if abs(diff_day * 24 * 60 * 60) <= 86400:
                times.append(abs(diff))
                time_day.append(False)
            else:
                times.append(abs(diff_day))
                time_day.append(True)

        comment_count = Comment.objects.all().filter(post=post).count()

        if comment_count > 1000 and comment_count < 1000000:
            comment_k = True
        elif comment_count > 1000000:
            comment_m = True

        context = {
            "post": post,
            "is_video": is_video,
            "is_text": is_text,
            "like_count": like_count,
            'is_like': is_like,
            "likes_person_two": likes_person_two,
            "comments": zip(comments, times, time_day),
            "comment_count": comment_count,
            "comment_k": comment_k,
            "comment_m": comment_m
        }
        return render(request, "home/comment.html", context)

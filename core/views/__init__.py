from index import index
from search import search

from register_user import register_user

from login_user import login_user
from logout_user import logout_user

from profile_detail import profile_detail
from profile_edit_photo import profile_edit_photo
from profile_link_new import profile_link_new
from profile_link_delete import profile_link_delete
from profile_invite import profile_invite
from profile_invite_thanks import profile_invite_thanks

from speaker_list import speaker_list
from user_follow import user_follow
from user_detail import UserDetail

from event_list import event_list
from event_detail import event_detail

from notification_detail import NotificationDetail
from notification_list import NotificationList

from rest_user_tag_list import UserTagList
from rest_user_link_detail import UserLinkDetail
from rest_user_tag_detail import UserTagDetail

__all__ = [
    "index", "search",
    "register_user", "login_user", "logout_user",
    "profile_detail", "profile_edit", "profile_edit_photo",
    "profile_link_new", "profile_link_delete",
    "profile_invite", "profile_invite_thanks",
    "speaker_list", "user_follow", "event_list", "event_detail",
    "UserDetail", "NotificationDetail", "NotificationList",
    "UserLinkDetail", "UserTagList", "UserTagDetail"
]

from index import index

from register_user import register_user
from register_speaker import register_speaker
from register_attendee import register_attendee
from register_event import register_event

from login_user import login_user
from logout_user import logout_user

from profile_detail import profile_detail
from profile_edit import profile_edit
from profile_edit_photo import profile_edit_photo
from profile_link_new import profile_link_new
from profile_tag_new import profile_tag_new

from speaker_list import speaker_list
from user_follow import user_follow

__all__ = [
    "index",
    "register_user", "login_user", "logout_user",
    'register_speaker', 'register_attendee', 'register_event',
    "profile_detail", "profile_edit", "profile_edit_photo",
    "profile_link_new", "profile_tag_new",
    "speaker_list", "user_follow",
]

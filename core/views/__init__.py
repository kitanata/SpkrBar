from index import index
from load_fixtures import load_fixtures

from register_user import register_user
from login_user import login_user
from logout_user import logout_user

from profile_archive import profile_archive
from profile_publish import profile_publish

from profile_edit import profile_edit
from profile_form_view import profile_form_view
from profile_edit_photo import profile_edit_photo
from profile_link_new import profile_link_new
from profile_tag_new import profile_tag_new

from speaker_list impor speaker_list
from speaker_detail import speaker_detail
from speaker_follow import speaker_follow

__all__ = [
    "index", "load_fixtures",
    "register_user", "login_user", "logout_user",
    "profile_archive", "profile_publish",
    "profile_edit", "profile_form_view", "profile_edit_photo",
    "profile_link_new", "profile_tag_new",
    "speaker_list", "speaker_detail", "speaker_follow",
]

from talk_archive import talk_archive
from talk_publish import talk_publish

from talk_new import talk_new
from talk_edit import talk_edit
from talk_delete import talk_delete
from talk_detail import talk_detail

from talk_comment_new import talk_comment_new
from talk_rate_new import talk_rate_new
from talk_endorsement_new import talk_endorsement_new

from talk_link_new import talk_link_new
from talk_link_delete import talk_link_delete
from talk_video_new import talk_video_new
from talk_photo_new import talk_photo_new
from talk_slides_new import talk_slides_new

from talk_submit import talk_submit
from talk_recruit import talk_recruit

from rest_talk_detail import TalkDetail
from rest_talk_tag_list import TalkTagList
from rest_talk_tag_detail import TalkTagDetail

__all__ = [
    "talk_archive", "talk_publish",
    "talk_new", "talk_edit", "talk_delete", "talk_detail",
    "talk_link_new", "talk_link_delete",
    "talk_comment_new", "talk_endorsement_new", "talk_rate_new",
    "talk_video_new", "talk_photo_new", "talk_slides_new",
    "talk_submit", "talk_recruit",
    "TalkDetail", "TalkTagList", "TalkTagDetail"]

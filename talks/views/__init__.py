from talk_new import talk_new
from talk_edit import talk_edit
from talk_delete import talk_delete
from talk_detail import talk_detail
from talk_list import talk_list

from talk_comment_new import talk_comment_new
from talk_endorsement_new import talk_endorsement_new

from talk_video_new import talk_video_new
from talk_slides_new import talk_slides_new

from rest_talk_detail import TalkDetail
from rest_talk_tag_list import TalkTagList
from rest_talk_tag_detail import TalkTagDetail

from rest_talk_link_list import TalkLinkList
from rest_talk_link_detail import TalkLinkDetail

from rest_talk_slide_deck_detail import TalkSlideDeckDetail
from rest_talk_video_detail import TalkVideoDetail
from rest_talk_comment_detail import TalkCommentDetail

__all__ = [
    "talk_list", "talk_new", "talk_edit", "talk_delete", "talk_detail",
    "talk_comment_new", "talk_endorsement_new", 
    "talk_video_new", "talk_photo_new", "talk_slides_new",
    "TalkDetail", 
    "TalkTagList", "TalkTagDetail",
    "TalkLinkList", "TalkLinkDetail",
    'TalkSlideDeckDetail', 'TalkVideoDetail',
    'TalkCommentDetail'
    ]

class BooleanQuest:
    def __init__(self, name, query=None):
        self.name = name
        self.query = query

    def __str__(self):
        return str(self.name)

    def process(self, user, value):
        params = query.split('.')

        model = user
        for param in params:
            if hasattr(model, param):
                attr = getattr(model, param)
                if type(attr) is FunctionType:
                    model = attr()
                else
                    model = attr

        if model == value:
            return 1
        else
            return 0


class NumericalQuest:
    def __init__(self, name, query=None):
        self.name = name
        self.user = user

    def __str__(self, value):
        return str(self.name) % value

    def process(self, user, value):
        params = query.split('.')

        model = user
        for param in params:
            if hasattr(model, param):
                attr = getattr(model, param)
                if type(attr) is FunctionType:
                    model = attr()
                else
                    model = attr

        if value:
            return self.num_completed / value
        else
            return 0


ProfilePhotoQuest = BooleanQuest(
        "Upload a photo to your profile.",
        query="get_profile.photo")


ProfileTalentQuest = NumericalQuest(
        "Add %d talents to your Profile",
        query="get_profile.tags.count")


InviteFriendsQuest = NumericalQuest(
        "Invite %d Friends",
        query="num_invites")


FollowFriendQuest = NumericalQuest(
        "Follow %d People",
        query="following.count")


AttainFollowerQuest = NumericalQuest(
        "Attain %d Followers",
        query="followers.count")


AttendTalkQuest = NumericalQuest(
        "Attend %d Talks",
        query='get_profile.attending.count')


EndorseTalkQuest = NumericalQuest(
        "Endorse %d Talks",
        query='talks_endorsed.count')


RateTalkQuest = NumericalQuest(
        "Rate %d Talks",
        query='talks_rated.count')


CommentTalkQuest = NumericalQuest(
        "Comment on %d Talks",
        query='talk_comments.count')


class QuestLevel:
    def __int__(self):
        self.cur_quest_name = "Quest Name Here"
        self.percent = 0.0

    def completed(self):
        return (self.percent == 1)

    def process(self, user):
        self.percent = 0.0
        for r, val in requirements.iteritems():
            self.percent += r.process(user, val)

        self.percent = self.percent / len(requirements.iteritems())

        return self.percent


class QuestLevelOne(QuestLevel):
    requirements = {
            ProfilePhotoQuest: "",
            ProfileTalentQuest: 3, 
            FollowFriendQuest: 3
            }

class QuestLevelTwo(QuestLevel):
    requirements = {
            AttendTalkQuest: 3,
            EndorseTalkQuest: 1,
            CommentTalkQuest: 1
            }

class QuestLevelThree(QuestLevel):
    requirements = {
            InviteFriendsQuest: 3,
            AttainFollowerQuest: 1,
            RateTalkQuest: 1
            }

class QuestLevelFour(QuestLevel):
    requirements = {
            AttendTalkQuest: 10,
            EndorseTalkQuest: 5,
            CommentTalkQuest: 5,
            RateTalkQuest: 3
            }

class QuestLevelFive(QuestLevel):
    requirements = {
            ProfileTalentQuest: 7,
            InviteFriendsQuest: 10,
            FollowFriendQuest: 10,
            AttainFollowerQuest: 5
            }


def quest_level_for_user(user):
    quests = [
            QuestLevelOne(),
            QuestLevelTwo(),
            QuestLevelThree(),
            QuestLevelFour(),
            QuestLevelFive()
            ]

    for quest in quests:
        percent = quest.process(user)

        if not quest.completed():
            return {quest.cur_quest_name: percent}

#class ProfileLinkQuest(Quest, NumericalQuestMixin):
#    Add 1 Link to Profile
#    pass

#class CreateTalkQuest(Quest, NumericalQuestMixin):
#    Create 1 Talk
#    pass

#class TalkSlidesQuest(Quest, NumericalQuestMixin):
#    Upload Slides to 1 Talk
#    pass

#class TalkVideoQuest(Quest, NumericalQuestMixin):
#    Upload Video to 1 Talk
#    pass

#class TalkPhotoQuest(Quest, ComplexNumericalQuestMixin):
#    Upload 3 Photos to 1 Talk
#    pass

#class TalkLinkQuest(Quest, ComplexNumericalQuestMixin):
#    Add 3 Links to 1 Talk
#    pass

#class TalkAttendanceQuest(Quest, ComplexNumericalQuestMixin):
#    Get 5 People to Attend 1 Talk
#    pass

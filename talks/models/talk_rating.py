from django.db import models
from datetime import datetime

class TalkRating(models.Model):
    #Engagement - Did the speaker keep attendees at the talk engaged and interested in the topic being presented?
    ENGAGE_RATING_CHOICES = (
        (1, "1 - I was bored throughout the entire presentation."),
        (2, "2 - I was NOT interested most of the time."),
        (3, "3 - The information was interesting but the presenter conveyed it poorly."),
        (4, "4 - The speaker was a skilled presenter and the information was interesting."),
        (5, "5 - This talk blew my mind. I am extremely excited about what I learned."))

    #Knowledge - Did the speaker seem extremely knowledgable on the subject?
    KNOWLEDGE_RATING_CHOICES = (
        (1, "1 - The speaker seemed vastly unprepared and didn't appear to know the subject."),
        (2, "2 - The topic seemed new to the speaker but they prepared the talk well."),
        (3, "3 - The speaker appeared to have personal experience with the topic."),
        (4, "4 - The speaker was knowledgable but did not seem to be an expert."),
        (5, "5 - The speaker was clearly an expert on the topic."))

    #Professionalism - Did the speaker remain professional throughout the talk?
    PROFESSIONAL_RATING_CHOICES = (
        (1, "1 - The talk included things I found offensive or wildly inappropriate."),
        (2, "2 - The speaker was rude, arrogant or aggressive"),
        (3, "3 - The speaker was kind but not nessecarily what I consider professional."),
        (4, "4 - The speaker was clearly professional and kind."),
        (5, "5 - The speaker exemplifies professionalism in my industry"))

    #Resources - Did the speaker offer external resources for attendees such as websites or presentation slides?
    RESOURCES_RATING_CHOICES = (
        (1, "1 - The speaker did not link to outside resources"),
        (2, "2 - The speaker provided links to their own blog, or social profiles."),
        (3, "3 - The speaker provided links to other blogs, research papers, and resources in addition to their own."),
        (4, "4 - The speaker provided many links and cited several of their sources."),
        (5, "5 - The speaker provided many links and cited every source of information."))

    #Discussion - Did the speaker encourage further discussion on the topic and answer questions appropriately?
    DISCUSSION_RATING_CHOICES = (
        (1, '1 - The speaker did not involve nor acknowledge the audience.'),
        (2, '2 - The speaker answered 1 or 2 questions at the end of the talk but did so poorly.'),
        (3, '3 - The speaker answered a few questions during the talk and at the end of the talk.'),
        (4, '4 - The speaker asked the audience questions and answered questions throughoughly.'),
        (5, '5 - The speaker involved everyone in the talk and encouraged continuing discussions beyond the event.'))

    talk = models.ForeignKey('Talk', related_name="ratings")
    rater = models.ForeignKey('core.SpkrbarUser', null=True)
    datetime = models.DateTimeField(default=datetime.now())

    engagement = models.IntegerField(choices=ENGAGE_RATING_CHOICES, default=1)
    knowledge = models.IntegerField(choices=KNOWLEDGE_RATING_CHOICES, default=1)
    professionalism = models.IntegerField(choices=PROFESSIONAL_RATING_CHOICES, default=1)
    resources = models.IntegerField(choices=RESOURCES_RATING_CHOICES, default=1)
    discussion = models.IntegerField(choices=DISCUSSION_RATING_CHOICES, default=1)

    engagement.verbose_name = "Engagement - Did the speaker keep attendees at the talk engaged and interested in the topic being presented?"
    knowledge.verbose_name = "Knowledge - Did the speaker seem extremely knowledgable on the subject?"
    professionalism.verbose_name = "Professionalism - Did the speaker remain professional throughout the talk?"
    resources.verbose_name = "Resources - Did the speaker offer external resources for attendees such as websites or presentation slides?"
    discussion.verbose_name = "Discussion - Did the speaker encourage further discussion on the topic and answer questions appropriately?"

    class Meta:
        app_label = 'talks'

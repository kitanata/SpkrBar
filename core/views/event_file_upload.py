import os
import csv
import xlrd
import json
import stripe

from collections import namedtuple
from dateutil.parser import parse as dtparse

from django.core.files import File
from django.template import loader, Context
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.core.validators import RegexValidator, URLValidator, validate_email, ValidationError

from core.models import EventUpload, EventUploadError, EventUploadSummary, EventUploadTypes
from core.models import SpkrbarUser, UserTag, UserLink
from core.helpers import save_file_with_uuid, assign_basic_permissions, send_html_mail, strip_tags

from talks.models import Talk, TalkTag, TalkLink, TalkSlideDeck, TalkVideo
from engagements.models import Engagement

stripe.api_key = settings.STRIPE_KEY

validate_url = URLValidator()

validate_at_handle = RegexValidator(r'^@\w*$')

email_template = loader.get_template('mail/claim_profile.html')

def validate_video_url(value):
    if not ('youtube' in value or 'vimeo' in value):
        raise ValidationError

    validate_url(value)

def validate_slide_url(value):
    if not ('slideshare' in value or 'speakerdeck' in value):
        raise ValidationError

    validate_url(value)

def validate_url_list(value):
    items = value.split(',')
    for item in items:
        validate_url(item)

def validate_date_or_time(value):
    try:
        dtparse(value)
    except:
        raise ValidationError

UploadColumnDefinition = namedtuple('UploadColumnDefinition', [
    'field_type', 'field_name', 'data_type', 'required'])

row_fields = [
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_TITLE, 'session_title', EventUploadTypes.DT_TEXT, True),
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_ABSTRACT, 'session_abstract', EventUploadTypes.DT_TEXT, False),
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_TAGS, 'session_tags', EventUploadTypes.DT_LIST_OF_TEXT, False),
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_VIDEO, 'session_video', EventUploadTypes.DT_URL_VIDEO, False),
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_SLIDE, 'session_slide', EventUploadTypes.DT_URL_SLIDE, False),
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_LINKS, 'session_links', EventUploadTypes.DT_LIST_OF_URLS, False),
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_DATE, 'session_date', EventUploadTypes.DT_DATE, True),
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_START_TIME, 'session_start_time', EventUploadTypes.DT_TIME, True),
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_END_TIME, 'session_end_time', EventUploadTypes.DT_TIME, True),
    UploadColumnDefinition(EventUploadTypes.COL_SESSION_ROOM_NAME, 'session_room_name', EventUploadTypes.DT_TEXT, True),
    UploadColumnDefinition(EventUploadTypes.COL_SPEAKER_NAME, 'speaker_name', EventUploadTypes.DT_TEXT, True),
    UploadColumnDefinition(EventUploadTypes.COL_SPEAKER_BIO, 'speaker_bio', EventUploadTypes.DT_TEXT, False),
    UploadColumnDefinition(EventUploadTypes.COL_SPEAKER_EMAIL, 'speaker_email', EventUploadTypes.DT_EMAIL, True),
    UploadColumnDefinition(EventUploadTypes.COL_SPEAKER_TAGS, 'speaker_tags', EventUploadTypes.DT_LIST_OF_TEXT, False),
    UploadColumnDefinition(EventUploadTypes.COL_SPEAKER_WEBSITE, 'speaker_website', EventUploadTypes.DT_URL, False),
    UploadColumnDefinition(EventUploadTypes.COL_SPEAKER_TWITTER, 'speaker_twitter', EventUploadTypes.DT_AT_HANDLE_OR_URL, False),
    UploadColumnDefinition(EventUploadTypes.COL_SPEAKER_FACEBOOK, 'speaker_facebook', EventUploadTypes.DT_URL, False),
    UploadColumnDefinition(EventUploadTypes.COL_SPEAKER_LINKEDIN, 'speaker_linkedin', EventUploadTypes.DT_URL, False)
]

_Row = namedtuple('_Row', [x.field_name for x in row_fields])

def validate_at_handle_or_url(value):
    try:
        validate_at_handle(value)
        return
    except ValidationError:
        pass

    validate_url(value)


validators = {
    EventUploadTypes.DT_TEXT: lambda x: True,
    EventUploadTypes.DT_EMAIL: validate_email,
    EventUploadTypes.DT_AT_HANDLE_OR_URL: validate_at_handle_or_url,
    EventUploadTypes.DT_LIST_OF_TEXT: lambda x: True,
    EventUploadTypes.DT_URL: validate_url,
    EventUploadTypes.DT_URL_VIDEO: validate_video_url,
    EventUploadTypes.DT_URL_SLIDE: validate_slide_url,
    EventUploadTypes.DT_LIST_OF_URLS: validate_url_list,
    EventUploadTypes.DT_DATE: validate_date_or_time,
    EventUploadTypes.DT_TIME: validate_date_or_time,
}

class Row(_Row):
    def __new__(cls, row_num, *fields):
        return super(Row, cls).__new__(cls, *fields)

    def __init__(self, row_num, *fields):
        super(Row, self).__init__(*fields)
        self.valid = False
        self.row_num = row_num

    def is_valid(self, import_model):
        self.valid = True
        for field in row_fields:
            field_value = getattr(self, field.field_name)

            #Test if it is required
            if field.required and not field_value:
                self.valid = False
                error = EventUploadError.requirement_error(import_model, self.row_num, field)
                error.save()

            #Test if the data type validates (DT_TEXT will always validate)
            if field_value:
                try:
                    validators[field.data_type](field_value)
                except ValidationError as e:
                    self.valid = False
                    error = EventUploadError.validation_error(import_model, self.row_num, field)
                    error.save()

        return self.valid


def build_summary(import_model, rows):
    num_sessions = len(rows)
    speaker_emails = set([row.speaker_email for row in rows])

    num_existing_speakers = 0
    num_new_speakers = 0

    for email in speaker_emails:
        if SpkrbarUser.objects.filter(email=email).exists():
            num_existing_speakers += 1
        else:
            num_new_speakers += 1

    tags = [row.session_tags.split(',') + row.speaker_tags.split(',') for row in rows]

    if tags:
        tags = reduce(lambda x, y: x + y, tags)
    num_tags = len(tags)
    num_unique_tags = len(set(tags))

    links = []
    for row in rows:
        links += row.session_links.split(',')

        if row.speaker_website:
            links += [row.speaker_website]

        if row.speaker_twitter:
            links += [row.speaker_twitter]

        if row.speaker_facebook:
            links += [row.speaker_facebook]

        if row.speaker_linkedin:
            links += [row.speaker_linkedin]

    if links:
        links = reduce(lambda x, y: x + y, links)

    num_links = len(links)
    num_unique_links = len(set(links))

    videos = [row.session_video for row in rows if row.session_video]
    slides = [row.session_slide for row in rows if row.session_slide]

    num_videos = len(videos)
    num_slides = len(slides)

    existing_sum = EventUploadSummary.objects.filter(event_upload=import_model)
    [o.delete() for o in existing_sum]

    EventUploadSummary.create(import_model, "Total Sessions",
        '{0} total sessions'.format(num_sessions)).save()
    EventUploadSummary.create(import_model, "Speakers",
        '{0} total speakers. {1} of them are new to SpkrBar!'.format(
            num_existing_speakers + num_new_speakers, num_new_speakers)).save()
    EventUploadSummary.create(import_model, "Tags and Topics",
        '{0} unique tags and topics. {1} total.'.format(
            num_unique_tags, num_tags)).save()
    EventUploadSummary.create(import_model, "Links to resources.",
        '{0} unique links to resources. {1} total.'.format(
            num_unique_links, num_links)).save()
    EventUploadSummary.create(import_model, "Videos",
        '{0} new videos.'.format(num_videos)).save()
    EventUploadSummary.create(import_model, "Slides",
        '{0} new slides.'.format(num_slides)).save()


def event_file_upload(request):
    if request.method != "POST" or not request.FILES:
        return HttpResponseBadRequest()

    upload_id = request.POST['upload_id'] 
    import_model = get_object_or_404(EventUpload, pk=upload_id)

    the_file = request.FILES['file']
    file_ext = the_file.name.split('.')[-1]

    if file_ext not in ['xls', 'xlsx', 'csv']:
        return HttpResponseBadRequest()

    file_name = save_file_with_uuid(the_file)

    if file_ext in ['xls', 'xlsx']:
        wb = xlrd.open_workbook(file_name)
        sh = wb.sheet_by_index(0)
        filename_root = file_name.split('.')[0]
        file_name = '.'.join([filename_root, 'csv'])
        csv_file = open(file_name, 'wb')
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        for rownum in xrange(sh.nrows):
            wr.writerow(sh.row_values(rownum))

        csv_file.close()

    full_file_name = os.path.join(settings.MEDIA_ROOT, file_name)

    import_model.import_file = File(open(full_file_name, "rb"))
    import_model.save()

    csv_reader = csv.reader(import_model.import_file)
    rows = [r for r in csv_reader]
    import_model.import_file.close()

    rows = [Row(num, *r) for num, r in enumerate(rows)]

    #Test if they deleted any of the example lines 1 through 5
    test_rows = rows[:5]
    bad_session_titles = ("Session Title", "Text", "REQUIRED", "", "Super Advanced Python")
    good_rows = [r for r in test_rows if r.session_title not in bad_session_titles]
    rows = good_rows + rows[5:]

    #Remove all the old errors
    [e.delete() for e in import_model.errors.all()]

    #Generate new ones based on validation
    data_valid = True
    for row in rows:
        if not row.is_valid(import_model):
            data_valid = False

    if data_valid:
        build_summary(import_model, rows)
        import_model.state = EventUpload.VALIDATION_SUCCESSFUL
        import_model.save()
        return render_to_response('upload_success.haml')
    else:
        import_model.state = EventUpload.VALIDATION_FAILED
        import_model.save()
        return render_to_response('upload_failed.haml')


def event_upload_confirm(request, pk):
    if request.method == "POST":
        token = request.POST['token']

        upload = get_object_or_404(request.user.uploads, pk=pk)

        if request.user.billed_forever:
            upload.user_billed = True
            upload.save()
            return process_event_upload(upload)

        if request.user.plan_name == 'yearly':
            if not upload.user_billed:
                try:
                    charge = stripe.Charge.create(
                        amount=60000,
                        currency="usd",
                        card=token,
                        description=request.user.email
                    )
                    upload.user_billed = True
                    upload.save()
                except stripe.CardError, e:
                    # The card has been declined
                    return HttpResponseBadRequest()
            return process_event_upload(upload)

        elif request.user.plan_name == 'forever':
            uploads = request.user.uploads.filter(user_billed=True)
            num_paid = len(uploads)
            forever_offer = 2400 - min((num_paid * 400), 1200)

            try:
                charge = stripe.Charge.create(
                    amount=forever_offer * 100,
                    currency="usd",
                    card=token,
                    description=request.user.email
                )
                request.user.billed_forever = True
                request.user.save()
                upload.user_billed = True
                upload.save()
                return process_event_upload(upload)
            except stripe.CardError, e:
                # The card has been declined
                return HttpResponseBadRequest()

    return HttpResponseNotFound()


def process_event_upload_speaker_link(speaker, type_name, url_target):
    if url_target and not speaker.links.filter(type_name=type_name, url_target=url_target).exists():
        link = UserLink()
        link.user = speaker
        link.type_name = type_name
        link.url_target = url_target
        link.save()


def process_event_upload_tags(model, klass, tag_string):
    if not tag_string:
        return

    tags = [t.strip() for t in tag_string.split(',')]

    for tag in tags:
        if len(tag) == 0:
            continue

        try:
            tag_instance = klass.objects.get(name=tag)
        except:
            tag_instance = klass()
            tag_instance.name = tag
            tag_instance.save()

        if tag_instance not in model.tags.all():
            model.tags.add(tag_instance)


def process_event_upload(upload):
    upload.state = EventUpload.IMPORT_STARTED
    upload.save()

    csv_reader = csv.reader(upload.import_file)
    rows = [r for r in csv_reader]
    upload.import_file.close()

    rows = [Row(num, *r) for num, r in enumerate(rows)]

    #Test if they deleted any of the example lines 1 through 5
    test_rows = rows[:5]
    bad_session_titles = ("Session Title", "Text", "REQUIRED", "", "Super Advanced Python")
    good_rows = [r for r in test_rows if r.session_title not in bad_session_titles]
    rows = good_rows + rows[5:]

    new_speakers = []
    for row in rows:
        try:
            speaker = SpkrbarUser.objects.get(email=row.speaker_email)
        except:
            password = SpkrbarUser.objects.make_random_password()
            speaker = SpkrbarUser.objects.create_user(row.speaker_email, password=password)
            speaker.save()
            new_speakers.append(speaker)

        if not speaker.full_name:
            speaker.full_name = strip_tags(row.speaker_name)

        if not speaker.about_me:
            speaker.about_me = strip_tags(row.speaker_bio)

        process_event_upload_tags(speaker, UserTag, strip_tags(row.speaker_tags))

        process_event_upload_speaker_link(speaker, 'LIN', row.speaker_linkedin)
        process_event_upload_speaker_link(speaker, 'TWI', row.speaker_twitter)
        process_event_upload_speaker_link(speaker, 'FAC', row.speaker_facebook)
        process_event_upload_speaker_link(speaker, 'WEB', row.speaker_website)

        speaker.save()

        try:
            talk = speaker.talks.get(name=row.session_title)
        except:
            talk = Talk()
            talk.speaker = speaker
            talk.name = strip_tags(row.session_title)

        if not talk.abstract:
            talk.abstract = strip_tags(row.session_abstract)

        talk.save()

        process_event_upload_tags(talk, TalkTag, strip_tags(row.session_tags))

        if row.session_video and talk.videos.count() == 0:
            video = TalkVideo.from_embed(talk, row.session_video)
            if video:
                video.save()

        if row.session_slide and talk.slides.count() == 0:
            deck = TalkSlideDeck.from_embed(talk, row.session_slide)
            if deck:
                deck.save()

        links = strip_tags(row.session_links).split(',')

        for l in links:
            if l and not talk.links.filter(url=l).exists():
                link = TalkLink()
                link.talk = talk
                link.name = "Session Resource"
                link.url = l
                link.save()

        start_date = dtparse(strip_tags(row.session_date))
        start_time = dtparse(strip_tags(row.session_start_time))

        eng = talk.engagements.filter(
            event_name=upload.name,
            date=start_date,
            time=start_time).exists()

        if not eng:
            en = Engagement()
            en.talk = talk
            en.speaker = speaker
            en.event_name = upload.name
            en.location = upload.location
            en.date = start_date
            en.time = start_time
            en.room = strip_tags(row.session_room_name)
            en.save()

    upload.state = EventUpload.IMPORT_FINISHED
    upload.save()

    #Notify every new speaker
    for speaker in new_speakers:
        assign_basic_permissions(speaker)

        mes = email_template.render(Context({'name': speaker.full_name, 'event': upload.name}))
        send_html_mail("Claim your profile on SpkrBar", strip_tags(mes), mes, [speaker.email])

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")

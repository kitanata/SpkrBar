import os
import csv
from collections import namedtuple
from dateutil.parser import parse as dtparse

from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.core.validators import RegexValidator, URLValidator, validate_email, ValidationError

from core.models import EventUpload, EventUploadError, EventUploadTypes
from core.helpers import save_file_with_uuid

validate_url = URLValidator()

validate_at_handle = RegexValidator(r'^@\w*$')

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


def event_file_upload(request):
    if request.method != "POST" or not request.FILES:
        return HttpResponseBadRequest()

    upload_id = request.POST['upload_id'] 
    import_model = get_object_or_404(EventUpload, pk=upload_id)

    the_file = request.FILES['file']
    file_name = save_file_with_uuid(the_file)
    full_file_name = os.path.join(settings.MEDIA_ROOT, file_name)

    rows = []
    with open(full_file_name, "rb") as f:
        csv_reader = csv.reader(f)
        rows = [r for r in csv_reader]

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
        import_model.state = EventUpload.VALIDATION_SUCCESSFUL
        import_model.save()
        return render_to_response('upload_success.haml')
    else:
        import_model.state = EventUpload.VALIDATION_FAILED
        import_model.save()
        return render_to_response('upload_failed.haml')

from django.db import models
from core.models import EventUpload

class EventUploadTypes:
    DT_TEXT = 'TEXT'
    DT_EMAIL = 'EMAIL'
    DT_AT_HANDLE_OR_URL = 'AT_HANDLE_OR_URL'
    DT_LIST_OF_TEXT = 'LIST_OF_TEXT'
    DT_URL = 'URL'
    DT_URL_VIDEO = 'URL_VIDEO'
    DT_URL_SLIDE = 'URL_SLIDE'
    DT_LIST_OF_URLS = 'LIST_OF_URLS'
    DT_DATE = 'DATE'
    DT_TIME = 'TIME'

    COL_SESSION_TITLE = 'SESSION_TITLE'             #REQUIRED    
    COL_SESSION_ABSTRACT = 'SESSION_ABSTRACT'       #OPTIONAL    
    COL_SESSION_TAGS = 'SESSION_TAGS'               #OPTIONAL    
    COL_SESSION_VIDEO = 'SESSION_VIDEO'             #OPTIONAL    
    COL_SESSION_SLIDE = 'SESSION_SLIDE'             #OPTIONAL    
    COL_SESSION_LINKS = 'SESSION_LINKS'             #OPTIONAL    
    COL_SESSION_DATE = 'SESSION_DATE'               #REQUIRED    
    COL_SESSION_START_TIME = 'SESSION_START_TIME'   #REQUIRED    
    COL_SESSION_END_TIME = 'SESSION_END_TIME'       #REQUIRED    
    COL_SESSION_ROOM_NAME = 'SESSION_ROOM_NAME'     #REQUIRED    
    COL_SPEAKER_NAME = 'SPEAKER_NAME'               #REQUIRED    
    COL_SPEAKER_BIO = 'SPEAKER_BIO'                 #OPTIONAL    
    COL_SPEAKER_EMAIL = 'SPEAKER_EMAIL'             #REQUIRED    
    COL_SPEAKER_TAGS = 'SPEAKER_TAGS'               #OPTIONAL
    COL_SPEAKER_WEBSITE = 'SPEAKER_WEBSITE'         #OPTIONAL
    COL_SPEAKER_TWITTER = 'SPEAKER_TWITTER'         #OPTIONAL
    COL_SPEAKER_FACEBOOK = 'SPEAKER_FACEBOOK'       #OPTIONAL
    COL_SPEAKER_LINKEDIN = 'SPEAKER_LINKEDIN'       #OPTIONAL

    ET_FIELD_REQUIRED = 'ERROR_FIELD_REQUIRED'
    ET_FIELD_PARSE_ERROR = 'ERROR_FIELD_PARSE_ERROR'

class EventUploadError(models.Model):
    DATA_TYPES = (
        (EventUploadTypes.DT_TEXT, EventUploadTypes.DT_TEXT),
        (EventUploadTypes.DT_EMAIL, EventUploadTypes.DT_EMAIL),
        (EventUploadTypes.DT_AT_HANDLE_OR_URL, EventUploadTypes.DT_AT_HANDLE_OR_URL),
        (EventUploadTypes.DT_LIST_OF_TEXT, EventUploadTypes.DT_LIST_OF_TEXT),
        (EventUploadTypes.DT_URL, EventUploadTypes.DT_URL),
        (EventUploadTypes.DT_URL_VIDEO, EventUploadTypes.DT_URL_VIDEO),
        (EventUploadTypes.DT_URL_SLIDE, EventUploadTypes.DT_URL_SLIDE),
        (EventUploadTypes.DT_LIST_OF_URLS, EventUploadTypes.DT_LIST_OF_URLS),
        (EventUploadTypes.DT_DATE, EventUploadTypes.DT_DATE),
        (EventUploadTypes.DT_TIME, EventUploadTypes.DT_TIME),
    )


    COLUMN_TYPES = (
        (EventUploadTypes.COL_SESSION_TITLE, EventUploadTypes.COL_SESSION_TITLE),
        (EventUploadTypes.COL_SESSION_ABSTRACT, EventUploadTypes.COL_SESSION_ABSTRACT),
        (EventUploadTypes.COL_SESSION_TAGS, EventUploadTypes.COL_SESSION_TAGS),
        (EventUploadTypes.COL_SESSION_VIDEO, EventUploadTypes.COL_SESSION_VIDEO),
        (EventUploadTypes.COL_SESSION_SLIDE, EventUploadTypes.COL_SESSION_SLIDE),
        (EventUploadTypes.COL_SESSION_LINKS, EventUploadTypes.COL_SESSION_LINKS),
        (EventUploadTypes.COL_SESSION_DATE, EventUploadTypes.COL_SESSION_DATE),
        (EventUploadTypes.COL_SESSION_START_TIME, EventUploadTypes.COL_SESSION_START_TIME),
        (EventUploadTypes.COL_SESSION_END_TIME, EventUploadTypes.COL_SESSION_END_TIME),
        (EventUploadTypes.COL_SESSION_ROOM_NAME, EventUploadTypes.COL_SESSION_ROOM_NAME),
        (EventUploadTypes.COL_SPEAKER_NAME, EventUploadTypes.COL_SPEAKER_NAME),
        (EventUploadTypes.COL_SPEAKER_BIO, EventUploadTypes.COL_SPEAKER_BIO),
        (EventUploadTypes.COL_SPEAKER_EMAIL, EventUploadTypes.COL_SPEAKER_EMAIL),
        (EventUploadTypes.COL_SPEAKER_TAGS, EventUploadTypes.COL_SPEAKER_TAGS),
        (EventUploadTypes.COL_SPEAKER_WEBSITE, EventUploadTypes.COL_SPEAKER_WEBSITE),
        (EventUploadTypes.COL_SPEAKER_TWITTER, EventUploadTypes.COL_SPEAKER_TWITTER),
        (EventUploadTypes.COL_SPEAKER_FACEBOOK, EventUploadTypes.COL_SPEAKER_FACEBOOK),
        (EventUploadTypes.COL_SPEAKER_LINKEDIN, EventUploadTypes.COL_SPEAKER_LINKEDIN),
    )

    ERROR_TYPES = (
        (EventUploadTypes.ET_FIELD_REQUIRED, EventUploadTypes.ET_FIELD_REQUIRED),
        (EventUploadTypes.ET_FIELD_PARSE_ERROR, EventUploadTypes.ET_FIELD_PARSE_ERROR),
    )

    event_upload = models.ForeignKey(EventUpload, related_name='errors')
    row = models.IntegerField()
    column = models.CharField(max_length=40, choices=COLUMN_TYPES)
    error_type = models.CharField(max_length=40, choices=ERROR_TYPES, default=EventUploadTypes.ET_FIELD_REQUIRED)
    expected_data_type = models.CharField(max_length=40, choices=DATA_TYPES)
    percieved_data_type = models.CharField(max_length=40, choices=DATA_TYPES, default=EventUploadTypes.DT_TEXT)

    class Meta:
        app_label = 'core'
        #states are 

    def __init__(self, import_model, row, column):
        self.event_upload = import_model
        self.row = row
        self.column = column.field_type

        return self

    @classmethod
    def requirement_error(cls, import_model, row, column):
        error = cls(import_model, row, column)
        error.error_type = EventUploadTypes.ET_FIELD_REQUIRED
        error.expected_data_type = EventUploadTypes.DT_TEXT
        error.percieved_data_type = EventUploadTypes.DT_TEXT

        return error

    @classmethod
    def validation_error(cls, import_model, row, column):
        error = cls(import_model, row, column)
        error.error_type = EventUploadTypes.ET_FIELD_REQUIRED
        error.expected_data_type = column.data_type
        error.percieved_data_type = EventUploadTypes.DT_TEXT

        return error

    def name_for_column(self):
        words = str(self.column).lower().split('_')
        return ' '.join([w.capitalize() for w in words])

    def name_for_expected_data_type(self):
        return self.name_for_data_type('expected_data_type')

    def name_for_percieved_data_type(self):
        return self.name_for_data_type('percieved_data_type')

    def name_for_data_type(self, field_name):
        field = getattr(self, field_name)

        field_name_map = {
            'TEXT': 'bunch of text',
            'EMAIL': 'email',
            'AT_HANDLE_OR_URL': '@handle or url',
            'LIST_OF_TEXT': 'list of text items separated by commas',
            'URL': 'url',
            'URL_VIDEO': 'url to youtube.com or vimeo.com',
            'URL_SLIDE': 'url to speakerdeck.com or slideshare.com',
            'LIST_OF_URLS': 'list of url items separated by commas',
            'DATE': 'date formatted like MM/DD/YYYY or MM/DD/YY',
            'TIME': 'time formatted like HH:MM AM/PM or HH:MM (24 hour)',
            'TIME_ZONE': 'a time zone (EST, CST, MST, PST)',
        }

        return field_name_map[str(field)]

    def __str__(self):
        if self.error_type == EventUploadError.ET_FIELD_REQUIRED:
            return "On row %d, the column %s is required." % int(self.row), self.name_for_column()
        elif self.error_type == EventUploadError.ET_FIELD_PARSE_ERROR:
            return "On row %d, the column %s should be a %s but it looks like a %s" % int(self.row), self.name_for_column(), self.name_for_expected_data_type(), self.name_for_percieved_data_type()
        else:
            return "Bummer. You aren't supposed to see this. You found a bug. Contact us at 407-590-1416 immediately."
        return self.name

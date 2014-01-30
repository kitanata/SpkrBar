from django.db import models

class EventUpload(models.Model):
    AT_REST = 'AT_REST'                               #Nothing has happened
    TEMPLATE_DOWNLOADED = 'TEMPLATE_DOWNLOADED'       #User downloaded the template
    VALIDATION_SUCCESSFUL = 'VALIDATION_SUCCESSFUL'   #Import validation was successful
    VALIDATION_FAILED = 'VALIDATION_FAILED'           #Import validation failed
    IMPORT_STARTED = 'IMPORT_STARTED'                 #Import queued for final processing
    IMPORT_FINISHED = 'IMPORT_FINISHED'               #Import has finished processing

    STATE_CHOICES = (
        (AT_REST, AT_REST),
        (TEMPLATE_DOWNLOADED, TEMPLATE_DOWNLOADED),
        (VALIDATION_SUCCESSFUL, VALIDATION_SUCCESSFUL),
        (VALIDATION_FAILED, VALIDATION_FAILED),
        (IMPORT_STARTED, IMPORT_STARTED),
        (IMPORT_FINISHED, IMPORT_FINISHED),
    )

    name = models.CharField(max_length=140)
    user = models.ForeignKey('core.SpkrbarUser', related_name='uploads')
    speakers = models.ManyToManyField('core.SpkrbarUser', related_name='event_imports')
    import_file = models.FileField(upload_to='event_imports')
    state = models.CharField(max_length=40, choices=STATE_CHOICES, default=AT_REST)
    user_billed = models.BooleanField(default=False)

    class Meta:
        app_label = 'core'
        #states are 

    def __str__(self):
        return self.name

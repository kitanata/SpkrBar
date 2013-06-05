import uuid
import os
from config.settings import MEDIA_ROOT

def save_photo_with_uuid(photo):
    photo_ext = photo.name.split('.')[-1]
    photo_root_name = str(uuid.uuid4()) + '.' + photo_ext
    photo_name = os.path.join('photo', photo_root_name)
    photo_storage = os.path.join(MEDIA_ROOT, 'photo', photo_root_name)

    with open(photo_storage, 'wb+') as destination:
        for chunk in photo.chunks():
            destination.write(chunk)

    return photo_name

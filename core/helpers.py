import uuid

def save_photo_with_uuid(photo):
    photo_ext = photo.name.split('.')[-1]
    photo_name = 'static/photo/' + str(uuid.uuid4()) + '.' + photo_ext

    with open(photo_name, 'wb+') as destination:
        for chunk in photo.chunks():
            destination.write(chunk)

    return photo_name

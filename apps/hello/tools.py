import json
import StringIO
from PIL import Image


def convert_to_json(form):
    if form.is_valid():
        json_ctx = dict({'ok': True})
    else:
        json_ctx = dict({'ok': False})
        json_ctx['errors'] = form.errors
    return json.dumps(json_ctx, encoding='utf-8', ensure_ascii=False)


def resize_photo(photo, width, height):
    img_file = StringIO.StringIO(photo.read())
    img = Image.open(img_file)
    photo_width, photo_height = img.size
    if photo_width > width or photo_height > height:
        proportion = photo_width/float(photo_height)
        if photo_width > photo_height:
            photo_width = width
            photo_height = int(photo_width / proportion)
        else:
            photo_height = height
            photo_width = int(photo_height * proportion)
        img = img.resize((photo_width, photo_height), Image.LANCZOS)
        img_file = StringIO.StringIO()
        img.save(img_file, 'JPEG', quality=90)
        photo.file = img_file

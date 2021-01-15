import string
from random import choice, randint

from PIL import Image
from flask import current_app


def handle(data):
    ext = data.filename.split('.')[-1]
    data = Image.open(data)
    output = (200, 200)
    data.thumbnail(output)
    character = string.digits + string.ascii_letters
    while True:
        try:
            x = "".join(choice(character) for x in range(randint(1, 2)))
            # if os.path.isfile(current_app.root_path + '/static/media/' + x + secure_filename(data.filename)):
            path = '/static/media/' + str(x) + '.' + ext
            data.save(current_app.root_path + path)
            if True:
                break
        except:
            pass
    return path

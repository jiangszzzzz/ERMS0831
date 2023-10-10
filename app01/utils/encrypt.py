from django.conf import settings
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode("UTF-8"))
    obj.update(data_string.encode("UTF-8"))
    return obj.hexdigest()

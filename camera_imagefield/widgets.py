import binascii
import mimetypes

import hashlib

import io

from datauri import DataURI
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms.widgets import FileInput
from django.utils.html import escape
from django.utils.safestring import mark_safe

__all__ = ['CameraImageWidget']


class CameraImageWidget(FileInput):

    def use_required_attribute(self, initial):
        return False

    def render(self, name, value, attrs=None, renderer=None):
        field = super(CameraImageWidget, self).render(name, value, attrs)
        return mark_safe("""<div class="camera-imagefield" data-name={}>{}</div>""".format(escape(name), field))


    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        if name in files:
            return files[name]
        elif '{}_data'.format(name) in data:
            try:
                file = DataURI(data['{}_data'.format(name)])
            except (ValueError, TypeError, binascii.Error):
                return None
            # file, field_name, name, content_type, size, charset,
            return InMemoryUploadedFile(file=io.BytesIO(file.data),
                                        field_name=name,
                                        name='{}{}'.format(hashlib.sha1(file.data).hexdigest(),
                                                           mimetypes.guess_extension(file.mimetype)),
                                        content_type=file.mimetype,
                                        size=len(file.data),
                                        charset=file.charset)


    class Media:
        css = {
            'all': ('camera_imagefield/camera_imagefield.css',)
        }
        js = ('camera_imagefield/camera_imagefield.js',)

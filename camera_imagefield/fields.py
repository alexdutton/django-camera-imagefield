import io
import math
import os.path

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from fractions import Fraction

from django import forms

from . import widgets

__all__ = ['CameraImageField']


class CameraImageField(forms.ImageField):
    widget = widgets.CameraImageWidget

    def __init__(self, *args, **kwargs):
        if 'aspect_ratio' in kwargs:
            self.min_aspect_ratio = self.max_aspect_ratio = kwargs.pop('aspect_ratio')
        else:
            self.min_aspect_ratio = kwargs.pop('min_aspect_ratio', None)
            self.max_aspect_ratio = kwargs.pop('max_aspect_ratio', None)

        self.max_size = kwargs.pop('max_size', None)
        self.prefer_jpeg = kwargs.pop('prefer_jpeg', False)

        super(CameraImageField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        file = super(CameraImageField, self).to_python(data)

        image = Image.open(file)
        image_format = 'jpeg' if self.prefer_jpeg else image.format

        aspect_ratio = Fraction(image.width, image.height)
        if self.min_aspect_ratio and aspect_ratio < self.min_aspect_ratio:
            new_height = image.height / self.min_aspect_ratio
            new_top = (image.height - new_height) / 2
            image = image.crop((0, new_top, image.width, new_top + new_height))
        elif self.max_aspect_ratio and aspect_ratio > self.max_aspect_ratio:
            new_width = image.height * self.max_aspect_ratio
            new_left = (image.width - new_width) / 2
            image = image.crop((new_left, 0, new_left + new_width, image.height))

        if self.max_size:
            if self.min_aspect_ratio and self.min_aspect_ratio == self.max_aspect_ratio:
                # If there's a fixed desired aspect ratio, then we're within subpixels of getting it right,
                # so let's resize to get the exact right size, as any stretching will have barely any effect.
                image = image.resize(self.max_size, Image.ANTIALIAS)
            else:
                # Otherwise, we can thumbnail, which will preserve the aspect ratio.
                image.thumbnail(self.max_size, Image.ANTIALIAS)

        if self.prefer_jpeg and image.mode in ('RGBA', 'LA'):
            # Remove the alpha channel, as JPEG doesn't support it
            background = Image.new(image.mode[:-1], image.size, (255, 255, 255))
            background.paste(image, image.split()[-1])
            image = background

        out = io.BytesIO()
        image.save(out, image_format)

        content_type = 'image/jpeg' if self.prefer_jpeg else file.content_type
        return InMemoryUploadedFile(file=out,
                                    field_name=file.field_name,
                                    name=os.path.splitext(file.name)[0] + '.jpeg' if self.prefer_jpeg else file.name,
                                    content_type=content_type,
                                    size=len(out.getvalue()),
                                    charset=file.charset)


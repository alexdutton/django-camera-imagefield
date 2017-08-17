from django import forms

from . import widgets

__all__ = ['CameraImageField']


class CameraImageField(forms.ImageField):
    widget = widgets.CameraImageWidget

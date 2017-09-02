# django-camera-imagefield

[![PyPI](https://img.shields.io/pypi/v/nine.svg)](https://pypi.python.org/pypi/django-camera-imagefield)

Django field and widget implementations that:

* Presents the user with the option to capture an image with their device's camera (e.g. laptop webcam or phone camera)
* Can enforce min/max aspect ratios by cropping
* Can enforce a maximum size constraint by resizing the uploaded image
* Can convert all image formats to JPEG if required

## Usage

```python
from fractions import Fraction

from camera_imagefield import CameraImageField
from django import forms


class MyForm(forms.Form):
    landscape = CameraImageField(aspect_ratio=Fraction(16, 9))
```

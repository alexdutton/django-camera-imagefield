# django-camera-imagefield

[![Build Status](https://travis-ci.org/alexsdutton/django-camera-imagefield.svg?branch=master)](https://travis-ci.org/alexsdutton/django-camera-imagefield) [![codecov](https://codecov.io/gh/alexsdutton/django-camera-imagefield/branch/master/graph/badge.svg)](https://codecov.io/gh/alexsdutton/django-camera-imagefield) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/55d2b6a967a94baa99a0bbb280527aef)](https://www.codacy.com/app/alexsdutton/django-camera-imagefield) [![PyPI](https://img.shields.io/pypi/v/django-camera-imagefield.svg)](https://pypi.python.org/pypi/django-camera-imagefield)

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

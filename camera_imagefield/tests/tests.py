from __future__ import division, unicode_literals

import math

import datauri
from fractions import Fraction
import io
import pkg_resources
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from ..fields import CameraImageField
from ..widgets import CameraImageWidget


class CameraImageFieldTestCase(TestCase):
    def setUp(self):
        self.test_image_data = io.BytesIO(pkg_resources.resource_string('camera_imagefield.tests',
                                                                        'data/ada-lovelace-chalon-portrait.jpg'))
        self.test_image = Image.open(self.test_image_data)
        self.test_image_data.seek(0)
        self.test_image_file = InMemoryUploadedFile(file=self.test_image_data,
                                                    field_name='file',
                                                    name='file.jpg',
                                                    content_type='image/jpeg',
                                                    size=len(self.test_image_data.getvalue()),
                                                    charset=None)

    def testInitialization(self):
        # Let's start simple
        self.assertIsInstance(CameraImageWidget(), CameraImageWidget)
        self.assertIsInstance(CameraImageField(), CameraImageField)

    def testPreferJPEG(self):
        png_data = io.BytesIO()
        self.test_image.save(png_data, 'png')
        png_data.seek(0)

        field = CameraImageField(prefer_jpeg=True)
        file = InMemoryUploadedFile(file=png_data,
                                    field_name='file',
                                    name='file.png',
                                    content_type='image/png',
                                    size=len(png_data.getvalue()),
                                    charset=None)
        new_file = field.to_python(file)

        new_image = Image.open(new_file)
        self.assertHTMLEqual('JPEG', new_image.format)

    def testCropAspectRatioPortrait(self):
        field = CameraImageField(max_aspect_ratio=Fraction(2, 3))
        new_file = field.to_python(self.test_image_file)
        new_image = Image.open(new_file)

        self.assertEqual(self.test_image.height, new_image.height)
        self.assertEqual(math.ceil(self.test_image.width * 2 / 3), new_image.width)

    def testCropAspectRatioLandscape(self):
        field = CameraImageField(min_aspect_ratio=Fraction(3, 2))
        new_file = field.to_python(self.test_image_file)
        new_image = Image.open(new_file)

        self.assertEqual(math.ceil(self.test_image.height * 2 / 3), new_image.height)
        self.assertEqual(self.test_image.width, new_image.width)

    def testMaxSize(self):
        field = CameraImageField(max_size=(200, 100))
        new_file = field.to_python(self.test_image_file)
        new_image = Image.open(new_file)

        # The image we uploaded was square, so this one should be too
        self.assertEqual((100, 100), new_image.size)


    def testMaxSizePortrait(self):
        field = CameraImageField(max_size=(100, 150), aspect_ratio=Fraction(2, 3))
        new_file = field.to_python(self.test_image_file)
        new_image = Image.open(new_file)

        # The image we uploaded was square, so this one should be too
        self.assertEqual((100, 150), new_image.size)

    def testPreferJPEGRemoveAlpha(self):
        image = Image.new('RGBA', (100, 100), (255, 0, 0, 128))
        image_data = io.BytesIO()
        image.save(image_data, 'PNG')
        image_data.seek(0)
        image_file = InMemoryUploadedFile(file=image_data,
                                                    field_name='file',
                                                    name='file.jpg',
                                                    content_type='image/png',
                                                    size=len(image_data.getvalue()),
                                                    charset=None)
        field = CameraImageField(prefer_jpeg=True)
        new_file = field.to_python(image_file)
        new_image = Image.open(new_file)
        self.assertEqual((255, 127, 126), new_image.getpixel((15, 5)))


class CameraImageWidgetTestCase(TestCase):
    def setUp(self):
        self.widget = CameraImageWidget()

    def test_value_from_datadict_file(self):
        file = InMemoryUploadedFile(io.BytesIO('foo'.encode()), 'file_one', 'file.txt', 'text/plain', 3, None)
        self.assertEqual(file, self.widget.value_from_datadict({}, {'file_one': file}, 'file_one'))

    def test_value_from_datadict_data(self):
        file_data = datauri.DataURI.make(mimetype='image/png', charset=None, base64=True, data='hello')
        file = self.widget.value_from_datadict({'file_one_data': file_data}, {}, 'file_one')
        self.assertEqual('hello'.encode(), file.read())
        self.assertEqual('image/png', file.content_type)

    def test_value_from_datadict_data_broken(self):
        file_data = datauri.DataURI.make(mimetype='image/png', charset=None, base64=True, data='hello')
        file_data = file_data[:-4] + file_data[-3:]
        self.assertEqual(None, self.widget.value_from_datadict({'file_one_data': file_data}, {}, 'file_one'))

    def test_render(self):
        rendered = self.widget.render('fieldname', None, {})
        self.assertTrue('fieldname' in rendered)

    def test_use_required_attribute(self):
        self.assertFalse(self.widget.use_required_attribute(None))

import math
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
        self.test_image_data.seek(0)
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

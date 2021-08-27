from pytest import mark, fixture
from app.app import convert_image
from pathlib import Path

image_folder_in_tests = Path(__file__).resolve().parent / 'image_folder_in_tests'


def test_convert_image():
    path = image_folder_in_tests
    filename = 'image_name.jpg'
    convert_image(image_folder_in_tests, 'image_name.jpg')

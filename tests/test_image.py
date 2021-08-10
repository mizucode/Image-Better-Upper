from pytest import mark, fixture
from app.app import allowed_file, clean_files, convert_image, prepare_images, DOWNLOAD_FOLDER, UPLOAD_FOLDER
import os
from zipfile import ZipFile
import PIL


def add_test_files(path, *names):
    os.chdir(path)
    for name in names:
        open(name, "a").close()
    file_list = os.listdir(path)
    assert set(names) <= set(file_list)

def add_jpg_to_convert(path, filename):
    im = PIL.Image.new(mode = "RGB", size = (200, 200),
                           color = (153, 153, 255))
    im.save(str(path / filename))


@mark.parametrize('filename, expected',
    [
        ('tattoo.jpg', True),
        ('elephant.png', True),
        ('nose.heic', False),
        ('wrong..jpg', True),
        ('.jpeg', True),
        ('some.file.png', True),
        ('png.tattoo', False),
    ]
)
def test_allowed_file_types(filename, expected):
    result = allowed_file(filename)

    assert result == expected


def test_clean_files():
    add_test_files(UPLOAD_FOLDER, 'test.jpg')
    add_test_files(DOWNLOAD_FOLDER, 'test.png')
    clean_files()
    upload_folder = os.listdir(UPLOAD_FOLDER)
    download_folder = os.listdir(DOWNLOAD_FOLDER)

    assert len(upload_folder) == 0
    assert len(download_folder) == 0

def test_convert_image():
    add_jpg_to_convert(UPLOAD_FOLDER, 'pil_img.jpg')
    convert_image(UPLOAD_FOLDER, 'pil_img.jpg')

    assert 'pil_img.png' in os.listdir(DOWNLOAD_FOLDER)

def test_prepare_images_only_compresses_png_files():
    add_test_files(DOWNLOAD_FOLDER, '1.jpg', '2.png', '3.png')
    zip_name = 'test_archive.zip'
    prepare_images(DOWNLOAD_FOLDER, zip_name)
    with ZipFile(DOWNLOAD_FOLDER / zip_name) as f:
        zipped_files = f.namelist()

    assert zip_name in os.listdir(DOWNLOAD_FOLDER)
    assert '2.png' in zipped_files
    assert '3.png' in zipped_files
    assert '1.jpg' not in zipped_files
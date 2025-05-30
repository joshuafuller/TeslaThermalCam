import pytest

pytest.importorskip('flask')
pytest.importorskip('cv2')

from TeslaThermalCam import generate_error_image


def test_generate_error_image_returns_nonempty_bytes():
    data = generate_error_image('test error')
    assert isinstance(data, (bytes, bytearray))
    assert len(data) > 0


def test_generate_error_image_handles_long_message():
    long_message = ' '.join(['error'] * 100)
    data = generate_error_image(long_message)
    assert isinstance(data, (bytes, bytearray))
    assert len(data) > 0
    import numpy as np
    import cv2
    img_array = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    assert image is not None
    assert image.shape == (192, 256, 3)

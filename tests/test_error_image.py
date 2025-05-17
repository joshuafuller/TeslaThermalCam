import pytest

from TeslaThermalCam import generate_error_image


def test_generate_error_image_returns_nonempty_bytes():
    pytest.importorskip('cv2')
    data = generate_error_image('test error')
    assert isinstance(data, (bytes, bytearray))
    assert len(data) > 0

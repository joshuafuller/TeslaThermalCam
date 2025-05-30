import pytest
import argparse
from unittest import mock

pytest.importorskip('flask')
pytest.importorskip('numpy')
pytest.importorskip('cv2')

with mock.patch.object(argparse.ArgumentParser, 'parse_args', return_value=argparse.Namespace(device=0)):
    from TeslaThermalCam import generate_error_image


def test_generate_error_image_returns_nonempty_bytes():
    pytest.importorskip('cv2')
    data = generate_error_image('test error')
    assert isinstance(data, (bytes, bytearray))
    assert len(data) > 0

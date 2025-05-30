import threading
import time
import argparse
from unittest import mock
import pytest

pytest.importorskip('flask')
pytest.importorskip('numpy')
pytest.importorskip('cv2')

with mock.patch.object(argparse.ArgumentParser, 'parse_args', return_value=argparse.Namespace(device=0)):
    import TeslaThermalCam as app_module
    from TeslaThermalCam import generate_frames, frame_lock


def test_generate_frames_yields_when_frame_updated():
    # Ensure shared state starts clean
    app_module.latest_frame = None

    gen = generate_frames()

    def update_frame():
        time.sleep(0.2)
        with frame_lock:
            app_module.latest_frame = b"fakejpg"

    t = threading.Thread(target=update_frame)
    t.start()

    frame = next(gen)
    gen.close()
    t.join()

    assert b"fakejpg" in frame

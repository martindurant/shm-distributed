import os
import subprocess
import shlex

import pytest


@pytest.fixture()
def lmdb_deleter():
    import shutil
    try:
        os.mkdir("/tmp/lmdb")
    except OSError:
        pass

    yield
    shutil.rmtree("/tmp/lmdb")


path = "/tmp/plasma"


@pytest.fixture(scope="module")
def plasma_process():
    pytest.importorskip("pyarrow.plasma")
    cmd = shlex.split(f"plasma-store-server -m 10000000 -s {path}")  # 10MB
    proc = subprocess.Popen(cmd)
    yield
    proc.terminate()
    proc.wait()


@pytest.fixture()
def plasma_session(plasma_process):
    from pyarrow import plasma

    timeout = 10
    while True:
        try:
            client = plasma.connect(path)
            client.list()
            break
        except (ValueError, TypeError, RuntimeError):
            timeout -= 0.1
            if timeout < 0:
                raise RuntimeError
            time.sleep(0.1)
    client.evict(1000000)
    yield client
    client.evict(1000000)

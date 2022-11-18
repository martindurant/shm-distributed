import os
import subprocess
import shlex
import shutil
import sys
import time

import pytest


plasma_path = "/tmp/plasma"
lmdb_path = "/tmp/lmdb"
vineyard_path = "/tmp/vineyard.sock"


@pytest.fixture(scope="module")
def lmdb_deleter():
    import shutil
    try:
        os.mkdir(lmdb_path)
    except OSError:
        pass

    yield
    shutil.rmtree(lmdb_path)


@pytest.fixture(scope="module")
def plasma_process():
    pytest.importorskip("pyarrow.plasma")
    plasma_exe = 'plasma-store-server'
    if shutil.which(plasma_exe) is None:
        plasma_exe = 'plasma_store'
    cmd = shlex.split(f"{plasma_exe} -m 10000000000 -s {plasma_path}")  # 10MB
    proc = subprocess.Popen(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    yield proc
    proc.terminate()
    proc.wait()


@pytest.fixture()
def plasma_session(plasma_process):
    from pyarrow import plasma

    timeout = 10
    while True:
        try:
            client = plasma.connect(plasma_path)
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


@pytest.fixture(scope="module")
def vineyard_process():
    pytest.importorskip("vineyard")
    cmd = [sys.executable, '-m', 'vineyard',
           '--socket', vineyard_path,
           '--size', '8331042816',
           '--meta', 'local']
    proc = subprocess.Popen(cmd)
    yield
    proc.terminate()
    proc.wait()


@pytest.fixture()
def vineyard_session(vineyard_process):
    import vineyard

    timeout = 10
    while True:
        try:
            client = vineyard.connect(vineyard_path)
            if client.connected:
                break
        except (ValueError, TypeError, RuntimeError):
            timeout -= 0.1
            if timeout < 0:
                raise RuntimeError
            time.sleep(0.1)
    yield client

import os
import numpy as np
import psutil
import pytest
import time

import distributed

from shm_distributed.utils import memories

MAX_ITER = 3
MEM_TOTAL = 2**30


def lmdb_connect():
    import lmdb
    return lmdb.open(
        path="/tmp/lmdb",
        map_size=100 * 2 ** 30,
        # sync=False,
        readahead=False,
        writemap=True,
        meminit=False,
        max_spare_txns=4,
        max_readers=16,
    )


@pytest.mark.parametrize(
    "size", [5, 5*2**20, 100*2**20, 3*2**30]
)
def test_lmdb_create_one(lmdb_deleter, size):
    data = bytearray(size)

    NITER = max(min(int(MEM_TOTAL / size), MAX_ITER), 1)
    t0 = time.time()
    for _ in range(NITER):
        lmdb = lmdb_connect()
        with lmdb.begin(write=True) as tcx:
            name = os.urandom(16)
            tcx.put(name, data)
        lmdb.close()
    print(f"{(time.time() - t0) / NITER:04f}")


@pytest.mark.parametrize("num", [10, 100, 1000, 5000])
def test_lmdb_create_many(lmdb_deleter, num):
    data = bytearray(10*2**20)
    t0 = time.time()
    lmdb = lmdb_connect()
    with lmdb.begin(write=True) as tcx:
        name = os.urandom(16)
        for _ in range(num):
            tcx.put(name, data)
    lmdb.close()
    print(f"{(time.time() - t0):04f}")


def client_scatter_workflow(client):
    data = np.empty(2**30, dtype="uint8")  # dropped at the end of this function
    f = client.scatter(data, broadcast=True)  # ephemeral ref in this process, which does not persist
    distributed.wait(f)
    return f  # be sure to capture return so that we don't clean up yet


def worker_scatter_workflow(client: distributed.Client):
    f = client.submit(np.empty, 2**30, dtype="uint8")
    client.replicate(f)
    distributed.wait(f)
    distributed.wait(client.map(lambda x, _: x[0], [f] * 4, list(range(4))))
    result = f.result()
    return f, result


@pytest.mark.parametrize("ser", ["pickle", "lmdb", "plasma"])
@pytest.mark.parametrize("workflow", [client_scatter_workflow, worker_scatter_workflow])
def test_workflow(ser, workflow, lmdb_deleter, plasma_session):
    client = distributed.Client(
        n_workers=4,
        threads_per_worker=1,
        serializers=[ser, "error"],
        worker_passthrough=dict(serializers=[ser, "error"]),
    )

    # ensure our config got through
    pids = list(client.run(os.getpid).values()) + [os.getpid()]
    if ser == "plasma":
        for proc in psutil.process_iter():
            if "plasma" in proc.name().lower():
                pids.append(proc.pid)
                break
    start_mem = memories(pids)
    mem0 = psutil.virtual_memory().used
    start_time = time.time()

    _ = workflow(client)
    time.sleep(1)

    end_mem = memories(pids)
    mem1 = psutil.virtual_memory().used
    end_time = time.time() - 1

    del _

    client.close()

    print(f"{end_time - start_time:03f}s")
    print("Start:", round(start_mem["rss"] / 2**20), "resident,", round(start_mem["uss"] / 2**20), "unique")
    print("Start:", round(end_mem["rss"] / 2**20), "resident,", round(end_mem["uss"] / 2**20), "unique")
    print("Δmem:", round((mem1 - mem0) / 2**20))

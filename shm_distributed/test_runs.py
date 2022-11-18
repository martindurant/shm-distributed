import os
import numpy as np
import psutil
import pytest
import time

import dask
import dask.array as da
import dask.dataframe as dd
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
    data = np.empty(2**29, dtype="uint8")  # dropped at the end of this function
    f = client.scatter(data, broadcast=True)  # ephemeral ref in this process, which does not persist
    del data
    f2 = client.submit(np.sum, client.map(lambda x, _: x[0], [f] * 6, list(range(6))))
    return f2


def worker_scatter_workflow(client: distributed.Client):
    f = client.submit(np.empty, 2**29, dtype="uint8")
    client.replicate(f)
    f2 = client.submit(np.sum, client.map(lambda x, _: x[0], [f] * 6, list(range(6))))
    return f2


def workflow_dataframe(client):
    ddf = dask.datasets.timeseries(
        dtypes={"name": "category", "id": int, "x": float, "y": float},
        freq="25ms"
    )
    f = client.persist(ddf.set_index("y").groupby("name").agg({"x": "std"})).to_delayed()[0]
    return client.submit(f)


def workflow_array(client):
    arr = da.ones(shape=(1000, 1000, 100), chunks=(200, 500, 50))
    arr2 = arr.map_overlap(lambda x: x + x.size, depth=5, boundary='reflect').sum()
    f = client.persist(arr2)
    f = np.atleast_1d(f.to_delayed())[0]
    return client.submit(f)


@pytest.mark.parametrize("ser", ["pickle", "lmdb", "plasma", "vineyard"])
@pytest.mark.parametrize("workflow", [workflow_dataframe, workflow_array,
                                      worker_scatter_workflow, client_scatter_workflow])
def test_workflow(ser, workflow, lmdb_deleter, plasma_session, vineyard_session, repeat=1):
    for _ in range(repeat):
        client = distributed.Client(
            n_workers=6,
            threads_per_worker=1,
            serializers=[ser, "error"],
            worker_passthrough=dict(serializers=[ser, "error"]),
            memory_limit=0
        )

        # ensure our config got through
        try:
            pids = list(client.run(os.getpid).values()) + [os.getpid()]
            if ser == "plasma" or ser == "vineyard":
                for proc in psutil.process_iter():
                    if "plasma" in proc.name().lower() or "vine" in proc.name().lower():
                        pids.append(proc.pid)
                        break
            start_mem = memories(pids)
            mem0 = psutil.virtual_memory().used
            start_time = time.time()

            memmax = mem0
            f = workflow(client)
            while not f.done():
                time.sleep(0.01)
                mem1 = psutil.virtual_memory().used
                if mem1 > memmax:
                    memmax = mem1

            end_mem = memories(pids)
            end_time = time.time()

        finally:
            client.close()
        time.sleep(7)  # cooldown time

    print("### ", ser, workflow.__name__)
    print(f"### {end_time - start_time:03f}s")
    print("### Start:", round(start_mem["rss"] / 2**20), "resident,", round(start_mem["uss"] / 2**20), "unique")
    print("### End:", round(end_mem["rss"] / 2**20), "resident,", round(end_mem["uss"] / 2**20), "unique")
    print("### Δmem:", round((mem1 - mem0) / 2**20))
    print("### Δmem_max:", round((memmax - mem0) / 2**20))
    print("###")

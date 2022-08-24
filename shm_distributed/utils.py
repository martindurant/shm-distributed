import os

import distributed
import psutil


def cluster(serializer):
    client = distributed.Client(
        n_workers=4,
        threads_per_worker=1,
        serializers=[serializer, "error"],
        worker_passthrough=dict(serializers=[serializer, "error"]),
    )
    return client, list(client.run(os.getpid).values())


def memories(pids):
    tot = {}
    for pid in pids:
        p = psutil.Process(pid)
        pinf = p.memory_full_info()
        for k in {"rss", "vms", "shared", "data", "uss", "pss"}:
            tot.setdefault(k, 0)
            tot[k] += getattr(pinf, k)
    return tot


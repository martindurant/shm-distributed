# shm-distributed
Benchmark and run scripts for shared memory on dask


### Preliminary results

```
shm_distributed/test_runs.py::test_workflow[worker_scatter_workflow-pickle] 2.765536s
Start: 602 resident, 370 unique
End: 4701 resident, 4471 unique
Δmem: 4147

shm_distributed/test_runs.py::test_workflow[worker_scatter_workflow-lmdb] 3.419665s
Start: 605 resident, 373 unique
End: 5727 resident, 1401 unique
Δmem: 1061

shm_distributed/test_runs.py::test_workflow[worker_scatter_workflow-plasma] 0.867145s
Start: 1649 resident, 1400 unique
End: 3700 resident, 3449 unique
Δmem: 1037

shm_distributed/test_runs.py::test_workflow[worker_scatter_workflow-vineyard] 0.783219s
Start: 1651 resident, 1401 unique
End: 4724 resident, 2426 unique
Δmem: 1041

shm_distributed/test_runs.py::test_workflow[client_scatter_workflow-pickle] 2.114218s
Start: 1631 resident, 1399 unique
End: 5729 resident, 5498 unique
Δmem: 4113

shm_distributed/test_runs.py::test_workflow[client_scatter_workflow-lmdb] 2.557086s
Start: 1634 resident, 1400 unique
End: 6757 resident, 1403 unique
Δmem: 15

shm_distributed/test_runs.py::test_workflow[client_scatter_workflow-plasma] 1.406608s
Start: 2677 resident, 2428 unique
End: 3703 resident, 3452 unique
Δmem: 5

shm_distributed/test_runs.py::test_workflow[client_scatter_workflow-vineyard] 1.543672s
Start: 3702 resident, 3452 unique
End: 4727 resident, 4477 unique
Δmem: 3

```

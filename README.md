# shm-distributed
Benchmark and run scripts for shared memory on dask


### Preliminary results

```
shm_distributed/test_runs.py::test_workflow_lmdb_scatter[client_scatter_workflow-pickle]
2.101000s
Start: 581 resident, 353 unique
Start: 4680 resident, 4453 unique
Δmem: 4145
PASSED

shm_distributed/test_runs.py::test_workflow_lmdb_scatter[client_scatter_workflow-lmdb]
2.649075s
Start: 583 resident, 356 unique
Start: 5704 resident, 357 unique
Δmem: 10
PASSED

shm_distributed/test_runs.py::test_workflow_lmdb_scatter[client_scatter_workflow-plasma]
1.649269s
Start: 1626 resident, 1383 unique
Start: 2652 resident, 2408 unique
Δmem: 1
PASSED

shm_distributed/test_runs.py::test_workflow_lmdb_scatter[worker_scatter_workflow-pickle]
2.803618s
Start: 2634 resident, 2406 unique
Start: 6732 resident, 6505 unique
Δmem: 4134
PASSED

shm_distributed/test_runs.py::test_workflow_lmdb_scatter[worker_scatter_workflow-lmdb]
3.790440s
Start: 2635 resident, 2407 unique
Start: 7760 resident, 4460 unique
Δmem: 1070
PASSED

shm_distributed/test_runs.py::test_workflow_lmdb_scatter[worker_scatter_workflow-plasma]
1.782626s
Start: 2653 resident, 2411 unique
Start: 5729 resident, 3437 unique
Δmem: 1023
PASSED
```

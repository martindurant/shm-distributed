# shm-distributed
Benchmark and run scripts for shared memory on dask


Preliminary results

```
 6.423957s
 Start: 1113 resident, 803 unique
 End: 3437 resident, 2810 unique
 Δmem: 1928
 Δmem_max: 2965

  lmdb workflow_dataframe
 5.792634s
 Start: 1127 resident, 817 unique
 End: 3786 resident, 3162 unique
 Δmem: 2359
 Δmem_max: 2890

  plasma workflow_dataframe
 6.032568s
 Start: 1147 resident, 834 unique
 End: 3594 resident, 2856 unique
 Δmem: 2221
 Δmem_max: 3090

  vineyard workflow_dataframe
 5.915032s
 Start: 1152 resident, 838 unique
 End: 3859 resident, 3221 unique
 Δmem: 2215
 Δmem_max: 2763

  pickle workflow_array
 0.554077s
 Start: 1141 resident, 830 unique
 End: 1678 resident, 1064 unique
 Δmem: 114
 Δmem_max: 114

  lmdb workflow_array
 0.313774s
 Start: 1145 resident, 835 unique
 End: 1507 resident, 883 unique
 Δmem: 96
 Δmem_max: 96

  plasma workflow_array
 0.304628s
 Start: 1165 resident, 851 unique
 End: 1527 resident, 901 unique
 Δmem: 98
 Δmem_max: 98

  vineyard workflow_array
 0.292848s
 Start: 1168 resident, 856 unique
 End: 1529 resident, 903 unique
 Δmem: 96
 Δmem_max: 96

  pickle worker_scatter_workflow
 0.523878s
 Start: 1157 resident, 847 unique
 End: 1157 resident, 847 unique
 Δmem: 12
 Δmem_max: 2612

  lmdb worker_scatter_workflow
 0.960925s
 Start: 1157 resident, 847 unique
 End: 3719 resident, 849 unique
 Δmem: 19
 Δmem_max: 532

  plasma worker_scatter_workflow
 1.243426s
 Start: 1174 resident, 860 unique
 End: 2712 resident, 2397 unique
 Δmem: 26
 Δmem_max: 538

  vineyard worker_scatter_workflow
 0.412534s
 Start: 1173 resident, 861 unique
 End: 2197 resident, 861 unique
 Δmem: 9
 Δmem_max: 522

  pickle client_scatter_workflow
 1.335742s
 Start: 1158 resident, 848 unique
 End: 1158 resident, 849 unique
 Δmem: 15
 Δmem_max: 3086

  lmdb client_scatter_workflow
 1.620295s
 Start: 1159 resident, 848 unique
 End: 4744 resident, 848 unique
 Δmem: 8
 Δmem_max: 8

  plasma client_scatter_workflow
 0.750103s
 Start: 1686 resident, 1374 unique
 End: 2199 resident, 1886 unique
 Δmem: 2
 Δmem_max: 2

  vineyard client_scatter_workflow
 0.791755s
 Start: 2199 resident, 1887 unique
 End: 2711 resident, 2398 unique
 Δmem: 4
 Δmem_max: 4

```

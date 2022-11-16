# shm-distributed
Benchmark and run scripts for shared memory on dask


Preliminary results

```
 pickle worker_scatter_workflow
1.598706s
Start: 897 resident, 571 unique
End: 1412 resident, 1086 unique
Δmem: 538

 lmdb worker_scatter_workflow
2.835939s
Start: 899 resident, 572 unique
End: 5511 resident, 1087 unique
Δmem: 43

 plasma worker_scatter_workflow
1.046257s
Start: 1431 resident, 1087 unique
End: 2970 resident, 2624 unique
Δmem: 530

 vineyard worker_scatter_workflow
0.802621s
Start: 1431 resident, 1086 unique
End: 3480 resident, 1087 unique
Δmem: 18

 pickle client_scatter_workflow
1.798240s
Start: 1411 resident, 1084 unique
End: 4485 resident, 4158 unique
Δmem: 3084

 lmdb client_scatter_workflow
1.399181s
Start: 1924 resident, 1596 unique
End: 5509 resident, 1597 unique
Δmem: 20

 plasma client_scatter_workflow
0.761663s
Start: 2967 resident, 2623 unique
End: 3481 resident, 3135 unique
Δmem: 13

 vineyard client_scatter_workflow
0.844939s
Start: 3991 resident, 3647 unique
End: 4504 resident, 4160 unique
Δmem: 8
```

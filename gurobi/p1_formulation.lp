\ Model Cloudlet-VM Allocation
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  allocate[c0,v1] + allocate[c0,v2] + allocate[c0,v3]
Subject To
 storage[c0]: 391 allocate[c0,v1] + 326 allocate[c0,v2]
   + 356 allocate[c0,v3] <= 5e+07
 storage[c1]: 391 allocate[c1,v1] + 326 allocate[c1,v2]
   + 356 allocate[c1,v3] <= 905
 storage[c2]: 391 allocate[c2,v1] + 326 allocate[c2,v2]
   + 356 allocate[c2,v3] <= 798
 storage[c3]: 391 allocate[c3,v1] + 326 allocate[c3,v2]
   + 356 allocate[c3,v3] <= 358
 storage[c4]: 391 allocate[c4,v1] + 326 allocate[c4,v2]
   + 356 allocate[c4,v3] <= 739
 CPU[c0]: 2046 allocate[c0,v1] + 2604 allocate[c0,v2]
   + 2731 allocate[c0,v3] <= 3e+06
 CPU[c1]: 2046 allocate[c1,v1] + 2604 allocate[c1,v2]
   + 2731 allocate[c1,v3] <= 4255
 CPU[c2]: 2046 allocate[c2,v1] + 2604 allocate[c2,v2]
   + 2731 allocate[c2,v3] <= 3443
 CPU[c3]: 2046 allocate[c3,v1] + 2604 allocate[c3,v2]
   + 2731 allocate[c3,v3] <= 6408
 CPU[c4]: 2046 allocate[c4,v1] + 2604 allocate[c4,v2]
   + 2731 allocate[c4,v3] <= 5890
 RAM[c0]: 118 allocate[c0,v1] + 246 allocate[c0,v2] + 134 allocate[c0,v3]
   <= 200000
 RAM[c1]: 118 allocate[c1,v1] + 246 allocate[c1,v2] + 134 allocate[c1,v3]
   <= 6794
 RAM[c2]: 118 allocate[c2,v1] + 246 allocate[c2,v2] + 134 allocate[c2,v3]
   <= 831
 RAM[c3]: 118 allocate[c3,v1] + 246 allocate[c3,v2] + 134 allocate[c3,v3]
   <= 2507
 RAM[c4]: 118 allocate[c4,v1] + 246 allocate[c4,v2] + 134 allocate[c4,v3]
   <= 5644
 allocate[v1]: allocate[c0,v1] + allocate[c1,v1] + allocate[c2,v1]
   + allocate[c3,v1] + allocate[c4,v1] = 1
 allocate[v2]: allocate[c0,v2] + allocate[c1,v2] + allocate[c2,v2]
   + allocate[c3,v2] + allocate[c4,v2] = 1
 allocate[v3]: allocate[c0,v3] + allocate[c1,v3] + allocate[c2,v3]
   + allocate[c3,v3] + allocate[c4,v3] = 1
Bounds
Binaries
 allocate[c0,v1] allocate[c0,v2] allocate[c0,v3] allocate[c1,v1]
 allocate[c1,v2] allocate[c1,v3] allocate[c2,v1] allocate[c2,v2]
 allocate[c2,v3] allocate[c3,v1] allocate[c3,v2] allocate[c3,v3]
 allocate[c4,v1] allocate[c4,v2] allocate[c4,v3]
End

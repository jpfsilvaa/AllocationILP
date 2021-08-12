\ Model Cloudlet-VM Allocation
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  30000 allocate[c0,v1] + 35000 allocate[c0,v2] + 35000 allocate[c0,v3]
   + 33000 allocate[c0,v4] + 30000 allocate[c0,v5] + 1500 allocate[c1,v2]
   + 1500 allocate[c1,v3] + 1200 allocate[c1,v4] + 1500 allocate[c2,v1]
   + 1000 allocate[c2,v4] + 1500 allocate[c2,v5] + 1200 allocate[c3,v1]
   + 1000 allocate[c3,v2] + 1000 allocate[c3,v3] + 1200 allocate[c3,v5]
Subject To
 storage[c0]: 150 allocate[c0,v1] + 150 allocate[c0,v2]
   + 170 allocate[c0,v3] + 180 allocate[c0,v4] + 190 allocate[c0,v5]
   <= 500000
 storage[c1]: 150 allocate[c1,v1] + 150 allocate[c1,v2]
   + 170 allocate[c1,v3] + 180 allocate[c1,v4] + 190 allocate[c1,v5]
   <= 510
 storage[c2]: 150 allocate[c2,v1] + 150 allocate[c2,v2]
   + 170 allocate[c2,v3] + 180 allocate[c2,v4] + 190 allocate[c2,v5]
   <= 520
 storage[c3]: 150 allocate[c3,v1] + 150 allocate[c3,v2]
   + 170 allocate[c3,v3] + 180 allocate[c3,v4] + 190 allocate[c3,v5]
   <= 530
 CPU[c0]: 2100 allocate[c0,v1] + 2200 allocate[c0,v2]
   + 2300 allocate[c0,v3] + 2400 allocate[c0,v4] + 2500 allocate[c0,v5]
   <= 3e+06
 CPU[c1]: 2100 allocate[c1,v1] + 2200 allocate[c1,v2]
   + 2300 allocate[c1,v3] + 2400 allocate[c1,v4] + 2500 allocate[c1,v5]
   <= 3100
 CPU[c2]: 2100 allocate[c2,v1] + 2200 allocate[c2,v2]
   + 2300 allocate[c2,v3] + 2400 allocate[c2,v4] + 2500 allocate[c2,v5]
   <= 3200
 CPU[c3]: 2100 allocate[c3,v1] + 2200 allocate[c3,v2]
   + 2300 allocate[c3,v3] + 2400 allocate[c3,v4] + 2500 allocate[c3,v5]
   <= 5300
 RAM[c0]: 120 allocate[c0,v1] + 220 allocate[c0,v2] + 320 allocate[c0,v3]
   + 420 allocate[c0,v4] + 520 allocate[c0,v5] <= 120000
 RAM[c1]: 120 allocate[c1,v1] + 220 allocate[c1,v2] + 320 allocate[c1,v3]
   + 420 allocate[c1,v4] + 520 allocate[c1,v5] <= 420
 RAM[c2]: 120 allocate[c2,v1] + 220 allocate[c2,v2] + 320 allocate[c2,v3]
   + 420 allocate[c2,v4] + 520 allocate[c2,v5] <= 540
 RAM[c3]: 120 allocate[c3,v1] + 220 allocate[c3,v2] + 320 allocate[c3,v3]
   + 420 allocate[c3,v4] + 520 allocate[c3,v5] <= 680
 allocate[v1]: allocate[c0,v1] + allocate[c1,v1] + allocate[c2,v1]
   + allocate[c3,v1] = 1
 allocate[v2]: allocate[c0,v2] + allocate[c1,v2] + allocate[c2,v2]
   + allocate[c3,v2] = 1
 allocate[v3]: allocate[c0,v3] + allocate[c1,v3] + allocate[c2,v3]
   + allocate[c3,v3] = 1
 allocate[v4]: allocate[c0,v4] + allocate[c1,v4] + allocate[c2,v4]
   + allocate[c3,v4] = 1
 allocate[v5]: allocate[c0,v5] + allocate[c1,v5] + allocate[c2,v5]
   + allocate[c3,v5] = 1
Bounds
Binaries
 allocate[c0,v1] allocate[c0,v2] allocate[c0,v3] allocate[c0,v4]
 allocate[c0,v5] allocate[c1,v1] allocate[c1,v2] allocate[c1,v3]
 allocate[c1,v4] allocate[c1,v5] allocate[c2,v1] allocate[c2,v2]
 allocate[c2,v3] allocate[c2,v4] allocate[c2,v5] allocate[c3,v1]
 allocate[c3,v2] allocate[c3,v3] allocate[c3,v4] allocate[c3,v5]
End

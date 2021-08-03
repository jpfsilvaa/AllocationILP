\ Model Delay Minimization
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  30000 allocation[c0,v1] + 35000 allocation[c0,v2]
   + 35000 allocation[c0,v3] + 33000 allocation[c0,v4]
   + 30000 allocation[c0,v5] + 1500 allocation[c1,v2]
   + 1500 allocation[c1,v3] + 1200 allocation[c1,v4]
   + 1500 allocation[c2,v1] + 1000 allocation[c2,v4]
   + 1500 allocation[c2,v5] + 1200 allocation[c3,v1]
   + 1000 allocation[c3,v2] + 1000 allocation[c3,v3]
   + 1200 allocation[c3,v5]
Subject To
 storage[c0]: 150 allocation[c0,v1] + 150 allocation[c0,v2]
   + 170 allocation[c0,v3] + 180 allocation[c0,v4] + 190 allocation[c0,v5]
   <= 500000
 storage[c1]: 150 allocation[c1,v1] + 150 allocation[c1,v2]
   + 170 allocation[c1,v3] + 180 allocation[c1,v4] + 190 allocation[c1,v5]
   <= 510
 storage[c2]: 150 allocation[c2,v1] + 150 allocation[c2,v2]
   + 170 allocation[c2,v3] + 180 allocation[c2,v4] + 190 allocation[c2,v5]
   <= 520
 storage[c3]: 150 allocation[c3,v1] + 150 allocation[c3,v2]
   + 170 allocation[c3,v3] + 180 allocation[c3,v4] + 190 allocation[c3,v5]
   <= 530
 CPU[c0]: 2100 allocation[c0,v1] + 2200 allocation[c0,v2]
   + 2300 allocation[c0,v3] + 2400 allocation[c0,v4]
   + 2500 allocation[c0,v5] <= 3e+06
 CPU[c1]: 2100 allocation[c1,v1] + 2200 allocation[c1,v2]
   + 2300 allocation[c1,v3] + 2400 allocation[c1,v4]
   + 2500 allocation[c1,v5] <= 3100
 CPU[c2]: 2100 allocation[c2,v1] + 2200 allocation[c2,v2]
   + 2300 allocation[c2,v3] + 2400 allocation[c2,v4]
   + 2500 allocation[c2,v5] <= 3200
 CPU[c3]: 2100 allocation[c3,v1] + 2200 allocation[c3,v2]
   + 2300 allocation[c3,v3] + 2400 allocation[c3,v4]
   + 2500 allocation[c3,v5] <= 5300
 RAM[c0]: 120 allocation[c0,v1] + 220 allocation[c0,v2]
   + 320 allocation[c0,v3] + 420 allocation[c0,v4] + 520 allocation[c0,v5]
   <= 120000
 RAM[c1]: 120 allocation[c1,v1] + 220 allocation[c1,v2]
   + 320 allocation[c1,v3] + 420 allocation[c1,v4] + 520 allocation[c1,v5]
   <= 420
 RAM[c2]: 120 allocation[c2,v1] + 220 allocation[c2,v2]
   + 320 allocation[c2,v3] + 420 allocation[c2,v4] + 520 allocation[c2,v5]
   <= 540
 RAM[c3]: 120 allocation[c3,v1] + 220 allocation[c3,v2]
   + 320 allocation[c3,v3] + 420 allocation[c3,v4] + 520 allocation[c3,v5]
   <= 680
 allocate[v1]: allocation[c0,v1] + allocation[c1,v1] + allocation[c2,v1]
   + allocation[c3,v1] = 1
 allocate[v2]: allocation[c0,v2] + allocation[c1,v2] + allocation[c2,v2]
   + allocation[c3,v2] = 1
 allocate[v3]: allocation[c0,v3] + allocation[c1,v3] + allocation[c2,v3]
   + allocation[c3,v3] = 1
 allocate[v4]: allocation[c0,v4] + allocation[c1,v4] + allocation[c2,v4]
   + allocation[c3,v4] = 1
 allocate[v5]: allocation[c0,v5] + allocation[c1,v5] + allocation[c2,v5]
   + allocation[c3,v5] = 1
Bounds
Binaries
 allocation[c0,v1] allocation[c0,v2] allocation[c0,v3] allocation[c0,v4]
 allocation[c0,v5] allocation[c1,v1] allocation[c1,v2] allocation[c1,v3]
 allocation[c1,v4] allocation[c1,v5] allocation[c2,v1] allocation[c2,v2]
 allocation[c2,v3] allocation[c2,v4] allocation[c2,v5] allocation[c3,v1]
 allocation[c3,v2] allocation[c3,v3] allocation[c3,v4] allocation[c3,v5]
End

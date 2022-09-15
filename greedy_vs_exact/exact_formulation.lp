\ Model Cloudlet-VM Allocation
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  211 allocate[cA,v0] + 195 allocate[cA,v1] + 180 allocate[cA,v2]
   + 180 allocate[cA,v3] + 108 allocate[cA,v4]
Subject To
 storage[cA]: 16384 allocate[cA,v0] + 16384 allocate[cA,v1]
   + 16384 allocate[cA,v2] + 16384 allocate[cA,v3] + 16384 allocate[cA,v4]
   <= 256000
 CPU[cA]: 16000 allocate[cA,v0] + 16000 allocate[cA,v1]
   + 32000 allocate[cA,v2] + 16000 allocate[cA,v3] + 8000 allocate[cA,v4]
   <= 24000
 RAM[cA]: 65536 allocate[cA,v0] + 65536 allocate[cA,v1]
   + 32768 allocate[cA,v2] + 65536 allocate[cA,v3] + 16384 allocate[cA,v4]
   <= 16384
Bounds
Binaries
 allocate[cA,v0] allocate[cA,v1] allocate[cA,v2] allocate[cA,v3]
 allocate[cA,v4]
End

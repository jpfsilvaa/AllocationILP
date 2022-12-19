cTypesU=(A_mult_small_100 A_mult_small_20 D_mult_mixed_20 D_mult_mixed_100)

for i in {0..3}
do
    for j in {0..99}
    do
        inFile=/home/jps/allocation_models/greedy_vs_exact/instances/vEta/cl${cTypesU[$i]}/inst_${j}.json
        python3 /home/jps/allocation_models/greedy_vs_exact/algorithms/greedy_alloc_v2_mult.py ${inFile} > /home/jps/allocation_models/greedy_vs_exact/results/vEta/greedy/cl${cTypesU[$i]}/inst_${j}.txt
    done
done
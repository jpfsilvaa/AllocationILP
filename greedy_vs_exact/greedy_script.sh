cTypesU=(A B C D E)
cTypesL=(a b c d e)

for i in {0..4}
do
    for j in {11..13}
    do
        python3 greedy_alloc_v2.py /home/jps/allocation_models/greedy_vs_exact/instances/vEpsilon/cl${cTypesU[i]}/cl${cTypesL[i]}_${j}.json > /home/jps/allocation_models/greedy_vs_exact/instances/vEpsilon/cl${cTypesU[i]}/cl${cTypesL[i]}_${j}.json
    done
done
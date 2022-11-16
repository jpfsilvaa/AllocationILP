cTypesU=(A B C D E)
cTypesL=(a b c d e)

for i in {0..4}
do
    for j in {11..30}
    do
        inFile=/home/jps/allocation_models/greedy_vs_exact/instances/vEpsilon/cl${cTypesU[i]}/cl${cTypesL[i]}_${j}.json
        python3 exact_alloc.py ${inFile} > /home/jps/allocation_models/greedy_vs_exact/results/vEpsilon/exact_epsilon_wPrice/cl${cTypesU[i]}/cl${cTypesL[i]}_${j}.txt
    done
done
cTypesU=(MMD_1 MMD_2)

for i in {0..1}
do
    for j in {0..99}
    do
        inFile=/home/jps/allocation_models/greedy_vs_exact/instances/vTheta/${cTypesU[$i]}/inst_${j}.json
        python3 /home/jps/allocation_models/greedy_vs_exact/algorithms/multipleKS/greedyAlloc.py ${inFile} > /home/jps/allocation_models/greedy_vs_exact/results/vTheta/greedyAlloc/${cTypesU[$i]}/inst_${j}.txt
    done
done
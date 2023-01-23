cTypesU=(100_10 200_20 300_30 400_40 500_50)

for i in {0..4}
do
    for j in {0..99}
    do
        inFile=/home/jps/allocation_models/greedy_vs_exact/instances/vIota/${cTypesU[$i]}/inst_${j}.json
        python3 /home/jps/allocation_models/greedy_vs_exact/algorithms/multipleKS/greedyMMD-4edge.py ${inFile} > /home/jps/allocation_models/greedy_vs_exact/results/vIota/greedyMMD/${cTypesU[$i]}/inst_${j}.txt
    done
done
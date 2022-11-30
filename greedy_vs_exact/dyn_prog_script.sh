cTypesU=(A B C D E)
cTypesL=(a b c d e)
cTypes_u=(A_gp1 A_mix E_200)
cTypes_l=(a_gp1 a_mix e_200)

for i in {0..2}
do
    for j in {0..99}
    do
        inFile=/home/jps/allocation_models/greedy_vs_exact/instances/vZeta/cl${cTypes_u[i]}/cl${cTypes_l[i]}_${j}.json
        python3 dyn_prog_alloc.py ${inFile} > /home/jps/allocation_models/greedy_vs_exact/results/vZeta/dynamic_programming/cl${cTypes_u[i]}/cl${cTypes_l[i]}_${j}.txt
    done
done
cTypesU=(A B C D E)
cTypesL=(a b c d e)
cTypes_u=(A_gp1 A_mix E_200)
cTypes_l=(a_gp1 a_mix e_200)


for j in {0..99}
do
    inFile=/home/jps/allocation_models/greedy_vs_exact/instances/vZeta/clE_10/cle_10_${j}.json
    python3 greedy_alloc.py ${inFile} > /home/jps/allocation_models/greedy_vs_exact/results/vZeta/greedy/clE_10/cle_10_${j}.txt
done

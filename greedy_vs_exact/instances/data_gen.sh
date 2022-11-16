seeds=(109 127 158 218 227 241 374 489 531 543 564 615 686 688 708 791 794 807 814 943)

for i in {0..19}
do
    fileNumber=$((i+11))
    python3 data_gen_.py 50 1 /home/jps/allocation_models/greedy_vs_exact/instances/vEpsilon/clE/cle_${fileNumber}.json ${seeds[i]}
done
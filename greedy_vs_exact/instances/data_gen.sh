seeds=(173 978 659 293 176 392 549 633 798 327 
        109 127 158 218 227 241 374 489 531 543 
        564 615 686 688 708 791 794 807 814 943 
        914 259 651 683 403 679 412 825 436 579 
        379 754 687 257 429 411 175 251 902 164 
        401 795 916 709 470 658 149 831 666 847 
        690 950 695 617 608 653 897 159 956 682 
        353 751 484 609 986 255 413 432 652 107 
        758 571 193 364 276 460 535 372 746 882 
        915 957 934 789 179 445 313 639 550 776)

for i in {0..99}
do
    fileNumber=$i
    python3 data_gen_mult.py 200 20 /home/jps/allocation_models/greedy_vs_exact/instances/vIota/500_50/inst_${fileNumber}.json ${seeds[i]}
done
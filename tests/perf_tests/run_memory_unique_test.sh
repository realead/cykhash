
K="000"
M="000000"
for fun_name in "pandas" "cykhash"
do
    echo $fun_name
    echo "number of elements\t overhead factor"
    for n in "1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20"
    do
          python memory_unique_test.py $fun_name $n$M
    done 
done 


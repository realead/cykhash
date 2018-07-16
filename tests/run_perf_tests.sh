WRAPPER="/usr/bin/time -fpeak_used_memory:%M(Kb)"

pip install numpy
pip install pandas


echo "\n\n-----Testing build-in test set\n\n"
for N  in "1000" "10000" "100000" "1000000" "10000000"
do
   $WRAPPER python perf_tests/mem_test_set.py $N
done 



echo "\n\n-----Testing build-in khash-set\n\n"
for N  in "1000" "10000" "100000" "1000000" "10000000"
do
   $WRAPPER python perf_tests/mem_test_khash.py $N
done  


echo "\n\n-----Testing pandas isin\n\n"
python perf_tests/isin_test.py



echo "\n\n-----Testing pandas unique\n\n"
for N  in "10000000" "20000000" "40000000" "60000000" "80000000"
do
    $WRAPPER python perf_tests/pandas_unique_test.py $N
    $WRAPPER python perf_tests/cyunique_test.py $N
done  




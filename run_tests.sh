#! /bin/bash

# if your tests fit the format of the other tests, you can register
# them here and include them in this script

Tests=("test0" "test1" "test2" "test3" "test4" "test5" "test6" "test7")
for t in ${Tests[*]}; do
    echo "compiling test $t"
    python3 main.py -lvn tests/${t}/${t}.cpp > tests/${t}/${t}ir.cpp
    cd tests/$t
    echo "compiling"
    make
    echo ""
    echo "running original, result:"
    ./original
    echo ""
    echo "running compiled, result:"
    ./compiled
    echo ""
    echo "----------"
    cd ../../
done


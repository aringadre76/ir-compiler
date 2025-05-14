
echo "compiling and running baseline"
python3 main.py tests/timing/timing.cpp > tests/timing/timing_ir.cpp
cd tests/timing
make
./driver
cd ../../

echo ""
echo "compiling and running with local value numbering"
python3 main.py -lvn tests/timing/timing.cpp > tests/timing/timing_ir.cpp
cd tests/timing
make
./driver
cd ../../

echo ""
echo "compiling and running with loop unrolling of 512"
python3 main.py -uf 512 tests/timing/timing.cpp > tests/timing/timing_ir.cpp
cd tests/timing
make
./driver
cd ../../

echo ""
echo "compiling and running with loop unrolling of 512 and local value numbering"
python3 main.py -lvn -uf 512 tests/timing/timing.cpp > tests/timing/timing_ir.cpp
cd tests/timing
make
./driver
cd ../../

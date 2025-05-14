#include <iostream>
using namespace std;

#include <chrono>
using namespace std::chrono;

#include "timing_ir.cpp"

int main() {
  int x,y;
  auto start = high_resolution_clock::now();
  for (int i = 0; i < 1024*16; i++)
      test7(x,y);
  auto stop = high_resolution_clock::now();

  auto duration = duration_cast<milliseconds>(stop - start);
 
  cout << "time (ms): " << duration.count() << endl;
  //cout << x << " " << y << endl;
  return 0;
}

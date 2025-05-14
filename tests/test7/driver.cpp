#include <iostream>
using namespace std;

// #if defined(IR)
// #include "test7ir.cpp"
// #else
// #include "test7.cpp"
// #endif

#include "test7ir.cpp"


int main() {
  int x,y;
  test7(x,y);
  cout << x << " " << y << endl;
  return 0;
}

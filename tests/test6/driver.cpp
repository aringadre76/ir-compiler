#include <iostream>
using namespace std;

#if defined(IR)
#include "test6ir.cpp"
#else
#include "test6.cpp"
#endif

int main() {
  int x,y;
  test6(x,y);
  cout << x << " " << y << endl;
  return 0;
}

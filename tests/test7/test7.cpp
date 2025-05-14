
void test7(int &x, int &y) {

  int i;
  int j;
  int k;  
  i = 1;
  j = 1;
  x = 0;
  y = 0;
  for (k = 0; k < 1024; k=k+1) {
    x = i + j;
    y = i + j;
  }
}

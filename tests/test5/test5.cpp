
void test5(int &x, int &y) {

  int i;
  i = 5;
  {
    int i;
    i = 6;
    {
      x = i;
    }
  }
  y = i;  
}


// LVN replaced 0 arithmetic instructions
#include "../../classir.h"
void test5(int &x,int &y){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg _new_name0;
virtual_reg _new_name1;
virtual_reg vr0_0;
virtual_reg _new_name0_3;
virtual_reg vr1_1;
virtual_reg _new_name1_2;
// LVN replaced 0 arithmetic instructions
vr0_0 = int2vr(5);
_new_name0 = vr0;
vr1_1 = int2vr(6);
_new_name1 = vr1;
x = vr2int(_new_name1_2);
y = vr2int(_new_name0_3);
return;
}
        

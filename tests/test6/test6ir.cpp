
// LVN replaced 1 arithmetic instructions
#include "../../classir.h"
void test6(int &x,int &y){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg vr4;
virtual_reg vr5;
virtual_reg vr6;
virtual_reg _new_name0;
virtual_reg _new_name1;
virtual_reg vr6_8;
virtual_reg vr1_1;
virtual_reg _new_name1_4;
virtual_reg vr3_5;
virtual_reg vr4_6;
virtual_reg vr2_2;
virtual_reg vr0_0;
virtual_reg vr5_7;
virtual_reg _new_name0_3;
// LVN replaced 1 arithmetic instructions
vr0_0 = int2vr(10);
_new_name1 = vr0;
vr1_1 = int2vr(10);
_new_name0 = vr1;
vr2_2 = addi(_new_name0_3,_new_name1_4);
x = vr2int(vr2_2);
vr3_5 = vr2_2;
y = vr2int(vr3_5);
vr4_6 = int2vr(x);
vr5_7 = int2vr(10);
vr6_8 = addi(vr4_6,vr5_7);
x = vr2int(vr6_8);
return;
}
        

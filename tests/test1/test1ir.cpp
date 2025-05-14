
// LVN replaced 0 arithmetic instructions
#include "../../classir.h"
void test1(int &x){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg vr4;
virtual_reg vr5;
virtual_reg vr6;
virtual_reg vr7;
virtual_reg vr8;

virtual_reg vr6_6;
virtual_reg vr0_0;
virtual_reg vr7_7;
virtual_reg vr5_5;
virtual_reg vr1_1;
virtual_reg vr3_3;
virtual_reg vr4_4;
virtual_reg vr8_8;
virtual_reg vr2_2;
// LVN replaced 0 arithmetic instructions
vr0_0 = int2vr(100);
vr1_1 = int2vr(1);
vr2_2 = int2vr(1);
vr3_3 = addi(vr1_1,vr2_2);
vr4_4 = int2vr(5);
vr5_5 = multi(vr3_3,vr4_4);
vr6_6 = int2vr(10);
vr7_7 = divi(vr5_5,vr6_6);
vr8_8 = addi(vr0_0,vr7_7);
x = vr2int(vr8_8);
return;
}
        

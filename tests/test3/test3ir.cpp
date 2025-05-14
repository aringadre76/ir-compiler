
// LVN replaced 0 arithmetic instructions
#include "../../classir.h"
void test2(int &x,int &y){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg vr4;
virtual_reg vr5;
virtual_reg vr6;

virtual_reg vr4_4;
virtual_reg vr0_0;
virtual_reg vr3_3;
virtual_reg vr1_1;
virtual_reg vr5_6;
virtual_reg vr2_2;
virtual_reg vr6_5;
// LVN replaced 0 arithmetic instructions
vr0_0 = int2vr(1);
vr1_1 = int2vr(0);
beq(vr0, vr1, label0);
vr2_2 = int2vr(1);
x = vr2int(vr2_2);
vr3_3 = int2vr(1);
y = vr2int(vr3_3);
branch(label1);
label0:
vr4_4 = int2vr(5);
x = vr2int(vr4_4);
vr5 = float2vr(5.0);
vr6_5 = vr_float2int(vr5_6);
y = vr2int(vr6_5);
label1:
return;
}
        

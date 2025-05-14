//expr_program: ['vr1 = int2vr(1024);', 'vr2 = lti(_new_name0,vr1);']
//original_assignment_program: ['vr0 = int2vr(0);', '_new_name0 = vr0;']
//loop_end_assignment_program: ['vr3 = int2vr(1);', 'vr4 = addi(_new_name0,vr3);', '_new_name0 = vr4;']
//val: 1024

// LVN replaced 0 arithmetic instructions
#include "../../classir.h"
void test4(float &x){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg vr4;
virtual_reg vr5;
virtual_reg vr6;
virtual_reg vr7;
virtual_reg vr8;
virtual_reg _new_name0;
virtual_reg vr6_6;
virtual_reg vr8_4;
virtual_reg _new_name0_3;
virtual_reg vr4_9;
virtual_reg vr7_7;
virtual_reg vr5_5;
virtual_reg vr2_2;
virtual_reg vr1_1;
virtual_reg vr0_0;
virtual_reg vr3_8;
// LVN replaced 0 arithmetic instructions
vr0_0 = int2vr(0);
_new_name0 = vr0;
label0:
vr1_1 = int2vr(1024);
vr2_2 = lti(_new_name0_3,vr1_1);
vr8_4 = int2vr(0);
beq(vr2, vr8, label1);
vr5_5 = float2vr(x);
vr6_6 = vr_int2float(_new_name0_3);
vr7_7 = addf(vr5_5,vr6_6);
x = vr2float(vr7_7);
vr3_8 = int2vr(1);
vr4_9 = addi(_new_name0_3,vr3_8);
_new_name0 = vr4;
branch(label0);
label1:
return;
}
        

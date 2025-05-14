
// LVN replaced 0 arithmetic instructions
#include "../../classir.h"
void test2(float &f0,float &f1){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;
virtual_reg vr3;
virtual_reg vr4;
virtual_reg vr5;
virtual_reg _new_name0;
virtual_reg _new_name1;
virtual_reg vr2_2;
virtual_reg vr3_3;
virtual_reg vr1_1;
virtual_reg _new_name0_5;
virtual_reg vr5_7;
virtual_reg vr0_0;
virtual_reg vr4_4;
virtual_reg _new_name1_6;
// LVN replaced 0 arithmetic instructions
vr0_0 = float2vr(f0);
vr1_1 = vr_float2int(vr0_0);
_new_name0 = vr1;
vr2_2 = float2vr(f1);
vr3_3 = vr_float2int(vr2_2);
_new_name1 = vr3;
vr4_4 = addi(_new_name0_5,_new_name1_6);
_new_name0 = vr4;
vr5_7 = vr_int2float(_new_name0_5);
f0 = vr2float(vr5_7);
return;
}
        

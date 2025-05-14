
// LVN replaced 0 arithmetic instructions
#include "../../classir.h"
void test0(int &a){
virtual_reg vr0;
virtual_reg vr1;
virtual_reg vr2;

virtual_reg vr2_2;
virtual_reg vr0_0;
virtual_reg vr1_1;
// LVN replaced 0 arithmetic instructions
vr0_0 = int2vr(a);
vr1_1 = int2vr(1);
vr2_2 = addi(vr0_0,vr1_1);
a = vr2int(vr2_2);
return;
}
        

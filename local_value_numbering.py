import re

def split_into_basic_blocks(program):
    basic_blocks = []
    current_block = []
    label_pattern = re.compile(r"^\s*label\d+:")
    branch_pattern = re.compile(r"^\s*branch\(label\d+\)")

    for instruction in program:
        if label_pattern.match(instruction):
            if current_block:
                basic_blocks.append(current_block)
            current_block = [instruction]
        elif branch_pattern.match(instruction):
            current_block.append(instruction)
            basic_blocks.append(current_block)
            current_block = []
        else:
            current_block.append(instruction)

    if current_block:
        basic_blocks.append(current_block)

    return basic_blocks

def parse_instruction(instruction):
    match = re.match(r'(\w+)\s*=\s*(\w+)\((\w+),?(\w+)?\);', instruction)
    if match:
        target = match.group(1)
        opcode = match.group(2)
        operand1 = match.group(3)
        operand2 = match.group(4)
        return (target, opcode, operand1, operand2)
    return None

def format_instruction(target, opcode, operand1, operand2):
    if operand2:
        return f"{target} = {opcode}({operand1},{operand2});"
    return f"{target} = {opcode}({operand1});"

def extract_parameters(program):
    header_pattern = re.compile(r"void\s+\w+\(([^)]+)\)")
    params_match = header_pattern.search("".join(program))
    parameters = []
    if params_match:
        params_str = params_match.group(1)
        parameters = [p.split("&")[-1].strip() for p in params_str.split(",")]
    return parameters

def number_variables(basic_blocks, parameters):
    global_counter = 0
    variable_numbering = {}
    new_variables = set()

    def get_variable_number(variable):
        nonlocal global_counter
        if variable is not None and variable not in parameters and (variable.startswith("vr") or variable.startswith("_new_name")):
            if variable not in variable_numbering:
                variable_numbering[variable] = f"{variable}_{global_counter}"
                global_counter += 1
            return variable_numbering[variable]
        return variable

    numbered_blocks = []
    for block in basic_blocks:
        numbered_block = []
        for instruction in block:
            parsed = parse_instruction(instruction)
            if parsed:
                target, opcode, operand1, operand2 = parsed
                target = get_variable_number(target)
                operand1 = get_variable_number(operand1)
                operand2 = get_variable_number(operand2)
                numbered_block.append(format_instruction(target, opcode, operand1, operand2))
                if target.startswith("vr") or target.startswith("_new_name"):
                    new_variables.add(target)
                if operand1 and (operand1.startswith("vr") or operand1.startswith("_new_name")):
                    new_variables.add(operand1)
                if operand2 and (operand2.startswith("vr") or operand2.startswith("_new_name")):
                    new_variables.add(operand2)
            else:
                numbered_block.append(instruction)
        numbered_blocks.append(numbered_block)

    return numbered_blocks, list(new_variables)

def patch_basic_blocks(basic_blocks, parameters):
    patched_blocks = []
    for block in basic_blocks:
        patched_block = []
        assignments = {}
        for instruction in block:
            parsed = parse_instruction(instruction)
            if parsed:
                target, opcode, operand1, operand2 = parsed
                if operand1 in assignments:
                    operand1 = assignments[operand1]
                if operand2 in assignments:
                    operand2 = assignments[operand2]
                patched_block.append(format_instruction(target, opcode, operand1, operand2))
                assignments[target] = target
            else:
                patched_block.append(instruction)
        patched_blocks.append(patched_block)
    return patched_blocks

def optimize_basic_blocks(basic_blocks):
    replaced_instructions = 0
    value_table = {}

    optimized_blocks = []
    for block in basic_blocks:
        optimized_block = []
        for instruction in block:
            parsed = parse_instruction(instruction)
            if parsed:
                target, opcode, operand1, operand2 = parsed
                if opcode in {'addi', 'subi', 'muli', 'divi'}:
                    if operand1.isdigit() or (operand2 and operand2.isdigit()):
                        optimized_block.append(instruction)
                    else:
                        expr_key = (opcode, operand1, operand2)
                        if expr_key in value_table:
                            if target == value_table[expr_key]:
                                optimized_block.append(f"{target} = {target};")
                            else:
                                optimized_block.append(f"{target} = {value_table[expr_key]};")
                            replaced_instructions += 1
                        else:
                            optimized_block.append(instruction)
                            value_table[expr_key] = target
                else:
                    optimized_block.append(instruction)
            else:
                optimized_block.append(instruction)
        optimized_blocks.append(optimized_block)

    return optimized_blocks, replaced_instructions

def LVN(program):
    parameters = extract_parameters(program)
    basic_blocks = split_into_basic_blocks(program)
    numbered_blocks, new_variables = number_variables(basic_blocks, parameters)
    patched_blocks = patch_basic_blocks(numbered_blocks, parameters)
    optimized_blocks, replaced_instructions = optimize_basic_blocks(patched_blocks)

    optimized_program = [instr for block in optimized_blocks for instr in block]

    # Add comment about replaced instructions
    #optimized_program.insert(0, f"// LVN replaced {replaced_instructions} arithmetic instructions")

    # Add declarations for new variables only once
    variable_declarations = [f"virtual_reg {var};" for var in new_variables]
    for i, line in enumerate(optimized_program):
        if line.startswith("virtual_reg"):
            optimized_program.insert(i, "\n".join(variable_declarations))
            break

    return optimized_program, new_variables, replaced_instructions

# Example IR Code
ir_code = [
    "#include \"../../classir.h\"",
    "void test1(int &x){",
    "virtual_reg vr0;",
    "virtual_reg vr1;",
    "virtual_reg vr2;",
    "virtual_reg vr3;",
    "virtual_reg vr4;",
    "virtual_reg vr5;",
    "virtual_reg vr6;",
    "virtual_reg vr7;",
    "virtual_reg vr8;",
    "vr0 = int2vr(100);",
    "vr1 = int2vr(1);",
    "vr2 = int2vr(1);",
    "vr3 = addi(vr1,vr2);",
    "vr4 = int2vr(5);",
    "vr5 = multi(vr3,vr4);",
    "vr6 = int2vr(10);",
    "vr7 = divi(vr5,vr6);",
    "vr8 = addi(vr0,vr7);",
    "x = vr2int(vr8);",
    "return;",
    "}"
]

optimized_ir, new_vars, replaced_count = LVN(ir_code)

# print("Optimized IR Code:")
# for line in optimized_ir:
#     print(line)
# print("\nNew Variables:", new_vars)
# print("Replaced Instructions:", replaced_count)

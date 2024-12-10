############################### MAIN FILE ########################################


def register_to_binary(register):   
    """Converts register name to binary."""
    reg_map = {
        "$zero": "0000","$t0": "0001", "$t1": "0010", "$t2": "0011", "$t3": "0100",
        "$t4": "0101","$sp": "0110"
    }
    return reg_map.get(register, "0000")


def r_type(opcode, rs, rt, rd, shamt):
    """Generates machine code for R-type instructions."""
    return f"{opcode}{register_to_binary(rs)}{register_to_binary(rt)}{register_to_binary(rd)}{shamt:04b}"


def i_type(opcode, rs, rt, immediate):
    """Generates machine code for I-type instructions."""
    return f"{opcode}{register_to_binary(rs)}{register_to_binary(rt)}{immediate:08b}"

def j_type(opcode, immediate, zero):
    
    #print("jump code ")
    #print(f"{opcode}{immediate: 08b}{zero: 08b}")
    # print(f"{immediate:08b}")
    return f"{opcode}{immediate:08b}{zero:08b}"


def parse_instruction(instruction):
    """Parses a single MIPS instruction and converts it to machine code."""
    initial_parts = instruction.replace(",", " ").split()
    instr = initial_parts[0]
    initial_parts= [part.strip() for part in initial_parts]
    parts= []
    for part in initial_parts:
        if part != " " or part != "":
            parts.append(part)
    
    if instr == "add":
        # add $d, $s, $t
        rd, rs, rt = parts[1], parts[2], parts[3]
        return r_type("1001", rs, rt, rd, 0)
    elif instr == "addi":
        # sub $d, $s, t
        rt, rs, val = parts[1], parts[2], parts[3]
        if(rs== "$sp" and rt == "$sp"):
            val= int(val)
        return i_type("1110", rs, rt, int(val))
    elif instr == "sub":
        # sub $d, $s, $t
        rd, rs, rt = parts[1], parts[2], parts[3]
        return r_type("1101", rs, rt, rd, 0)
    elif instr == "subi":
        # subi $d, $s, $t
        rt, rs, val = parts[1], parts[2], parts[3]
        return i_type("1000", rs, rt, int(val))
    elif instr == "and":
        # and $d, $s, $t
        rd, rs, rt = parts[1], parts[2], parts[3]
        return r_type("0001", rs, rt, rd, 0)
    elif instr == "andi":
        # andi $d, $s, $t
        # rd, rs, rt = parts[1], parts[2], parts[3]
        rt, rs, val = parts[1], parts[2], parts[3]
        return i_type("0010", rs, rt, int(val))
    elif instr == "or":
        # or $d, $s, $t
        rd, rs, rt = parts[1], parts[2], parts[3]
        return r_type("0101", rs, rt, rd, 0)
    elif instr == "ori":
        # ori $d, $s, $t
        # rd, rs, rt = parts[1], parts[2], parts[3]
        rt, rs, val = parts[1], parts[2], parts[3]
        return i_type("1010", rs, rt, int(val))
    elif instr == "lw":
        # lw $t, offset($s)
        rt, offset_reg = parts[1], parts[2]
        offset, rs = offset_reg.split("(")
        rs = rs.rstrip(")")
        return i_type("0111", rs, rt, int(offset))
    elif instr == "sw":
        # sw $t, offset($s)
        rt, offset_reg = parts[1], parts[2]
        offset, rs = offset_reg.split("(")
        rs = rs.rstrip(")")
        return i_type("0000", rs, rt, int(offset))
    
    elif instr == "sll":
        # sll $d, $t, shamt
        rt, rs, shamt = parts[1], parts[2], int(parts[3])
        rd="0000"
        return r_type("0110",rs, rt, rd, shamt)
    
    elif instr == "srl":
        # srl $d, $t, shamt
        rt, rs, shamt = parts[1], parts[2], int(parts[3])
        rd="0000"
        return r_type("1011",rs, rt, rd, shamt)
    
    elif instr == "nor":
        # nor $d, $s, $t
        rd, rs, rt = parts[1], parts[2], parts[3]
        return r_type("0100", rs, rt, rd, 0)
    
    elif instr == "beq":
        # beq $s, $t, offset
        rt, rs, offset = parts[1], parts[2], int(parts[3])
        return i_type("1100", rs, rt, offset)
    
    elif instr == "bneq":
        # bneq $s, $t, offset
        rt, rs, offset = parts[1], parts[2], int(parts[3])
        return i_type("1111", rs, rt, offset)
    
    elif instr == "j":
        # j target
        target = int(parts[1])
        # print(parts[1])
        return j_type("0011", target, 0)
    
    else:
        raise ValueError(f"Unsupported instruction: {instruction}")
    


def to_hex(parsed):
    print(parsed)
    if "-" in parsed:
        parsed2, parsed = parsed.split("-")[0], parsed.split("-")[1]  
        length = len(parsed)
        # print(parsed)
        decimal = int(parsed, 2)
        two_complement = (1 << length) - decimal
        # print(bin(two_complement))
        if(length < 8):
            two_complement = two_complement + 2**length
        # print(bin(two_complement)[2:])
        # print("hex is: ")
        # print(hex(-two_complement) )
        return hex(int(parsed2,2))+hex(-two_complement)[3:] 
    else:
        return hex(int(parsed2,2))+hex(int(parsed.replace(" ", ""), 2))[2:] 
    

def assemble(mips_code):
    """Assembles a list of MIPS instructions into machine code."""
    machine_code = []
    for line in mips_code:
        line = line.strip()
        if line and not line.startswith("#"):  
            parsed = parse_instruction(line)
            # print(parsed)
            if "-" in parsed:  
                hex_value = to_hex(parsed)
                # print(hex_value)  
                machine_code.append(hex_value)  
            else:
                hex_value = hex(int(parsed.replace(" ", ""), 2))
                machine_code.append(hex_value)
                
    return machine_code


def read_mips_code(file_path):
    mips_code = []
    with open(file_path, 'r') as file:
        for line in file:

            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                mips_code.append(stripped_line)
    
    return mips_code


def load_mips_code_to_array(input_file):
    mips_code_array = []
    
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:
                mips_code_array.append(stripped_line)
    
    return mips_code_array


def get_label_line_numbers(mips_code):
    label_line_numbers = {}
    label_count = 0

    for line_number, line in enumerate(mips_code):
        if line.strip().endswith(':'):
            label = line.strip().rstrip(':').lstrip('0') 
            label_line_numbers[label] = line_number - label_count
            label_count += 1
    
    return label_line_numbers

def remove_labels(mips_code):
    return [line for line in mips_code if not line.strip().endswith(':')]


def replace_labels_with_line_numbers(mips_code, label_line_numbers):
    updated_mips_code = []

    for line_number, line in enumerate(mips_code):
        if line.strip().endswith(":"):
            continue

        updated_line = line 
        for label, label_line in label_line_numbers.items():
            if label in line:  
                if "beq" in line or "bneq" in line:
                    offset = label_line - line_number - 1
                    updated_line = line.replace(label, str(offset))
                    # print(f"Updated branch: {line.strip()} -> {updated_line.strip()}")
                    break
                elif "j" in line:  # Jump instruction
                    updated_line = line.replace(label, str(label_line))
                    # print(f"Updated jump: {line.strip()} -> {updated_line.strip()}")
                    break

        updated_mips_code.append(updated_line)

    return updated_mips_code


file_path = 'B1_05_Necessary_Content\input.asm.txt'
mips_code = read_mips_code(file_path)


# removing comments
with open('mips_cleaned.txt', 'w') as file:
        file.write("addi $sp, $sp, -1 " + '\n')
        for line in mips_code:
            code = line
            if len(code) < 5:
                code = code.zfill(5)
            file.write(code + '\n')

input_filename = 'mips_cleaned.txt' 

# loading the code into array
mips_code_array = load_mips_code_to_array(input_filename)

#  extracting labells
label_line_numbers = get_label_line_numbers(mips_code_array)

for label, line_number in label_line_numbers.items():
    print(f"Label: {label}, Line Number: {line_number}")

mips_code_array = remove_labels(mips_code_array)
print("--------------")
mips_code_labelled= replace_labels_with_line_numbers(mips_code_array, label_line_numbers)
for line in mips_code_labelled:
    print(line)


with open('instruction_formatted.txt', 'w') as file:
        for line in mips_code_labelled:
            file.write(line + '\n')
print("Instruction formatted file written")
machine_code = assemble(mips_code_labelled)

with open('instruction_image.txt', 'w') as file:
        file.write("v2.0 raw\n")
        for line in machine_code:
            code = line[2:]
            code = code.replace(" ", "")
            if len(code) < 5:
                code = code.zfill(5)
            file.write(code + '\n')
print("Instruction image created")
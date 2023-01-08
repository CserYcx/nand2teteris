""" The Task Steps:
    1. Read the .asm file every line
    2. Ignore the white spaces and slashes
    3. Assemble the instructions(A-instruction/C-instruction)
"""

# Use the command line to programme, you can do python Assembler.py "filepath"
import sys
import os.path

# Record the line number
line_count = 0

# File path
final_path = "test.hack"
pre_path = "pre.txt"

# The number begins to allocate the register number
begin = 16

number_list = ['0','1','2','3','4','5','6','7','8','9']

symbol_table = {
    # The pre-defined symbol 
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SP":  0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN":16384,
    "KBD":  24576
}

# Return a file object
def read_file():
    if len(sys.argv) != 2:
        print("The parameter is not enough!!!")

    # The read file path
    filepath = sys.argv[1]
    return open(filepath)

# Return a file which can write the translated binary to a file
def write_file(s):
    if os.path.isfile(s) is False:
        return open(s,"w")
    return open(s,"w") 

# Parse the every line
def parse(line):
    """
    You have to remove the annotation first!!!!!!!
    """
    # If current line is annotation, ignore it and return null string
    if is_annotation(line):
        return "" 
    # If current line is blank, do the same thing like annotation
    elif is_blank(line):
        return ""
    # split the line 
    instruction = [ch for ch in line if ch != " "]
    if is_Ainstr(instruction):
        return Ainstr_binary(instruction)
    elif is_Cinstr(instruction):
        return Cinstr_binary(instruction)
    # If current line is segment, update the dict and 
    # You have to recognize all the segment position
    elif is_segment(instruction):
        return ""
    # the instruction is error
    else:
        AssertionError(None)

# If current line is jump sign(like (LOOP),(END))
def is_segment(instruction):
    if instruction[0] == '(' and instruction[len(instruction)-2] == ')':
        #print("The instruction is segment")
        return True
    return False

# Update the segment into the symbol_table
def update_seg(instruction):
    segment = get_expr(instruction)
    segment = ''.join(segment[1:len(segment)-1])
    seg_dict = {segment: line_count}
    symbol_table.update(seg_dict)
    
        
# Return true if instruction is A-instruction
def is_Ainstr(instruction):
    if instruction[0] == '@':
        return True
    return False

# Return true if instruction is C-instruction
def is_Cinstr(instruction):
    return not is_Ainstr(instruction) and not is_segment(instruction)

# Return a list which has the main expression
# Example: as an A-instruction, return @symbol
# As a C-instruction, return A=A+1 or D;JMP
def get_expr(instruction):
    new_instruction = remove_annotation(instruction)
    expr = []
    for num in new_instruction:
        if num == "\n":
            continue
        else:
            expr.append(num)
    #print(expr)
    return expr

# Remove the annotation and return a new list
def remove_annotation(instruction):
    expr = []
    for ch in instruction:
        if ch == '/':
            break
        elif ch == ' ':
            continue
        else:
            expr.append(ch)
    return expr

# Translate the C-instruction and return binary code
def Cinstr_binary(instruction):
    flag = Cinstr_type(instruction)
    if flag == 0:
        return comp_binary(instruction)
    elif flag == 1:
        return jump_binary(instruction)

# Translate C-instruction to the jump-type
def jump_binary(instruction):
    expr = get_expr(instruction)
    pre,back = get_pre_back(expr)
    back = ''.join(back)
    #print(back)
    """
    Here are my fix code
    """
    opcode = "111"
    a_c_bit = comp(pre)
    d_bit = "000"
    j_bit = "000"
    if back == "JGT":
        j_bit = "001"
    elif back == "JEQ":
        j_bit = "010"
    elif back == "JGE":
        j_bit = "011"
    elif back == "JLT":
        j_bit = "100"
    elif back == "JNE":
        j_bit = "101"
    elif back == "JLE":
        j_bit = "110"
    elif back == "JMP":
        j_bit = "111"
    else :
        print("The jump instruction is illegl")
        assert(0)
    return opcode+a_c_bit+d_bit+j_bit

# Get the pre-expression and back-expression, seperated by the compute symbol
# You have to remove the annotation
def get_pre_back(instruction):
    pos = 0
    for ch in instruction:
        if ch == '=':
            break
        elif ch == ';':
            break
        pos += 1
    pre = instruction[0:pos]
    back = instruction[pos+1:]
    return pre,back

# Translate C-instruction to the comp-type
def comp_binary(instruction):
    # pos to record the '=' position
    expr = get_expr(instruction)
    pre,back = get_pre_back(expr) 
    opcode = "111"
    a_c_bit = comp(back)
    d_bit = dest(pre)
    j_bit = "000"
    return opcode+a_c_bit+d_bit+j_bit

# Translate the back-expr to the code which show how to compute the expression
def comp(back_expr):
    a_bit = "0"
    for ch in back_expr:
        if ch == 'A':
            a_bit = "0"
        elif ch == 'M':
            a_bit = "1"
    string = ''.join(back_expr)
    c_bit = "000000"
    if string == "0":
        c_bit = "101010"
    elif string == "1":
        c_bit = "111111"
    elif string == "-1":
        c_bit = "111010"
    elif string == "D":
        c_bit = "001100"
    elif string == "A" or string == "M":
        c_bit = "110000"
    elif string == "!D":
        c_bit = "001101"
    elif string == "!A" or string == "!M":
        c_bit = "110001"
    elif string == "-D":
        c_bit = "001111"
    elif string == "-A" or string == "-M":
        c_bit = "110011"
    elif string == "D+1":
        c_bit = "011111"
    elif string == "A+1" or string == "M+1":
        c_bit = "110111"
    elif string == "D-1":
        c_bit = "001110"
    elif string == "A-1" or string == "M-1":
        c_bit = "110010"
    elif string == "D+A" or string == "D+M":
        c_bit = "000010"
    elif string == "D-A" or string == "D-M":
        c_bit = "010011"
    elif string == "A-D" or string == "M-D":
        c_bit = "000111"
    elif string == "D&A" or string == "D&M":
        c_bit = "000000"
    elif string == "D|A" or string == "D|M":
        c_bit = "010101"

    return a_bit+c_bit

# Translate the pre-expr to the code pointing to the destination
def dest(pre_expr):
    string = ''.join(pre_expr)
    if string == "M":
        return "001"
    elif string == "D":
        return "010"
    elif string == "MD":
        return "011"
    elif string == "A":
        return "100"
    elif string == "AM":
        return "101"
    elif string == "AD":
        return "110"
    elif string == "AMD":
        return "111"
    else:
        return "000"


# If instruction is computing, return 0 
# Else return 1, instruction is jumping
def Cinstr_type(instruction):
    for ch in instruction:
        if ch == '=':
            return 0
        elif ch == ';':
            return 1
        else:
            continue
    print("The C-instruction is illegal!")

# Translate the A-instruction and return binary code
# No symbol table (Then i have to fix it)

def Ainstr_binary(instruction):
    symbol = get_expr(instruction)[1:]
    """
    If symbol is number, transfer it to the binary code
    If symbol is not number:
    1. Look up the symbol_table, if symbol key exists: get the key value
    2. Else, add the key to the symbol_table
    """
    # If symbol is number
    if symbol[0] in number_list:
        # Convert the list to string to int, and transfert the decimal to the binary
        # That's the no symbol method
        number = "".join(symbol)
        code = int(number)
        code_binary = to_binary(code)

    # Symbol is symbol
    else:
        symbol = ''.join(symbol)
        global begin
        # If sysmbol exists, get the symbol's value
        if symbol_table.get(symbol) is not None:
            code_binary = to_binary(symbol_table.get(symbol))
        # Else update the symbol_table and return the binary code of begin
        else:
            new_dict = {symbol: begin}
            symbol_table.update(new_dict)
            code_binary = to_binary(begin)
            begin += 1
    return code_binary

# Change the decimal to the binary code
def to_binary(number):
    print("The segment number is ",number)
    binary = bin(number)[2:]
    symbol_binary = binary.rjust(15,'0')
    Ainstr_binary = '0'
    return Ainstr_binary + symbol_binary

# Return true if line is annotation, else return false
def is_annotation(line):
    if line[0] == '/' and line[1] == '/':
        return True
    return False

# Return true if line is blanket
def is_blank(line):
    return line[0] == '\n'

"""
    The main code here:
"""

# readfile is the file you want to translate
# writefile is the file you've translated
readfile = read_file()
writefile = write_file(final_path)

"""
    The fix code and reason:
    Why to repair it because i forget to pre-define the segment
    That's a horrible error(Shit!!!)
"""
# Pre-treat the line and update the symbol_table
for line in readfile:
    instruction = [ch for ch in line if ch != " "]
    if is_segment(instruction):
        update_seg(instruction)
        continue
    elif is_annotation(line):
        continue
    elif is_blank(line):
        continue
    line_count += 1

# Reopen the file
readfile = read_file()
line_count = 0
# The main things have to do:
# The iterator of line will ignore the blank
for line in readfile:
    # Parse every line and translate them to the 16-bits binary 
    # output is a list type
    output = parse(line)            
    print(output)
    if(output == ""):
        continue
    writefile.write(str(output)+"\n")
    line_count += 1

# The Test
print(symbol_table)


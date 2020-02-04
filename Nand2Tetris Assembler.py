'''Opens a file with a Hack program written in assembly, removes all comments 
and whitespace, and passes the remaining lines of text into a list, with each 
line a separate element of this list.'''

def open_and_clean_text(n):
    y = open(n)
    text = y.readlines()
    separator = '//'
    for i in range(0, len(text)):
        text[i] = text[i].rstrip('\n')
        text[i] = text[i].replace(' ', '')
        text[i] = text[i].split(separator, 1)[0]
        i = 0
    j = len(text)
    while i < j:
        if text[i] == '' or text[i][0] == '/':
            del text[i]
            j -= 1
        else:
            i += 1
    return text

'''When iterated over a list whose elements are Hack assembly commands, returns
the command type of each line'''

def commandType(n):
    if n[0] == '@':
        return 'A_COMMAND'
    elif n[0] == '(':
        return 'SYMBOL'
    else:
        return 'C_COMMAND'

'''Given a Hack assembly A instruction or label symbol declaration, 
returns the portion of the instruction needed for further processing'''

def symbol(n):
    if n[-1] == ')':
        return n[1:-1]
    else:
        return n[1::]

'''Returns the destination mnemonic of a Hack assembly C instruction'''

def dest(n):
    x = n.find('=')
    if x == -1:
        return ''
    else:
        return n[0:x]

'''Returns the computation mnemonic of a Hack assembly C instruction'''

def comp(n):
    x = n.find('=')
    y = n.find(';')
    if y == -1:
        return n[x+1::]
    else:
        return n[x+1:y]

'''Returns the jump mnemonic of a Hack assembly C instruction'''

def jump(n):
    x = n.find(';')
    if x == -1:
        return ''
    else:
        return n[x+1::]

'''Converts a Hack assembly destination mnemonic to its binary equivalent'''

def dest_binary(n):
    if n == '':
        return '000'
    elif n == 'M':
        return '001'
    elif n == 'D':
        return '010'
    elif n == 'MD':
        return '011'
    elif n == 'A':
        return '100'
    elif n == 'AM':
        return '101'
    elif n == 'AD':
        return '110'
    else:
        return '111'

'''Converts a Hack assembly computation mnemonic to its binary equivalent'''
 
def comp_binary(n):
    if n == '0':
        return '0101010'
    elif n == '1':
        return '0111111'
    elif n == '-1':
        return '0111010'
    elif n == 'D':
        return '0001100'
    elif n == 'A':
        return '0110000'
    elif n == '!D':
        return '0001101'
    elif n == '!A':
        return '0110001'
    elif n == '-D':
        return '0001111'
    elif n == '-A':
        return '0110011'
    elif n == 'D+1':
        return '0011111'
    elif n == 'A+1':
        return '0110111'
    elif n == 'D-1':
        return '0001110'
    elif n == 'A-1':
        return '0110010'
    elif n == 'D+A':
        return '0000010'
    elif n == 'D-A':
        return '0010011'
    elif n == 'A-D':
        return '0000111'
    elif n == 'D&A':
        return '0000000'
    elif n == 'D|A':
        return '0010101'
    elif n == 'M':
        return '1110000'
    elif n == '!M':
        return '1110001'
    elif n == '-M':
        return '1110011'
    elif n == 'M+1':
        return '1110111'
    elif n == 'M-1':
        return '1110010'
    elif n == 'D+M':
        return '1000010'
    elif n == 'D-M':
        return '1010011'
    elif n == 'M-D':
        return '1000111'
    elif n == 'D&M':
        return '1000000'
    else:
        return '1010101'

'''Converts a Hack assembly jump mnemonic to its binary equivalent'''

def jump_binary(n):
    if n == '':
        return '000'
    elif n == 'JGT':
        return '001'
    elif n == 'JEQ':
        return '010'
    elif n == 'JGE':
        return '011'
    elif n == 'JLT':
        return '100'
    elif n == 'JNE':
        return '101'
    elif n == 'JLE':
        return '110'
    else:
        return '111'
#%%
'''Takes an input file name of type .asm containing a Hack computer program
written in the Hack assembly language and an output file name of type .hack. 
Converts the assembly program in the input .asm file to its Hack machine 
language equivalent and writes the converted machine language instructions to         
the .hack file'''

def assembler(input_file, output_file):
    '''initializes the symbol table, creates counters for potentially needed 
    RAM and ROM addresses, and creates an array in which the converted machine
    language instructions will be placed for eventual writing to the given 
    .hack file'''
    
    symbol_table = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 
                    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5,
                    'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
                    'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 
                    'SCREEN': 16384, 'KBD': 24576}
    ROM_address = 0
    RAM_address = 15
    converted_commands = []
    clean_text = open_and_clean_text(input_file)
    
    '''Passes through the assembly program and adds all symbol labels to the
    symbol table, assigning to each the relevant ROM address'''
    
    for i in range(0, len(clean_text)):
        if commandType(clean_text[i]) == 'SYMBOL':
            symbol_table[clean_text[i][1:-1]] = ROM_address
        else:
            ROM_address += 1
    
    '''Passes through the assembly program, converting all instructions to 
    their Hack machine language equivalents and adding them to the 
    converted_commands array in preparation for writing the converted program
    to the given .hack output file'''
    
    for i in range(0, len(clean_text)):
        cT = commandType(clean_text[i]) 
        if cT == 'A_COMMAND':
            x = symbol(clean_text[i])
            if x.isdigit() == False:
                if (x in symbol_table) == True:
                    y = symbol_table[x]
                    binary_y = format(int(y), 'b')
                    num_frontal_zeros_y = 16-len(binary_y)
                    binary16_y = '0'*num_frontal_zeros_y + binary_y
                    converted_commands.append(binary16_y)
                else:
                    symbol_table[x] = RAM_address + 1
                    RAM_address += 1
                    z = symbol_table[x]
                    binary_z = format(int(z), 'b')
                    num_frontal_zeros_z = 16-len(binary_z)
                    binary16_z = '0'*num_frontal_zeros_z + binary_z
                    converted_commands.append(binary16_z)
                    
            else:
                binary_num = format(int(symbol(clean_text[i])), 'b')
                num_frontal_zeros = 16-len(binary_num)
                binary_num = '0'*num_frontal_zeros + binary_num
                converted_commands.append(binary_num)
        
        elif cT == 'C_COMMAND':
            x = dest_binary(dest(clean_text[i]))
            y = comp_binary(comp(clean_text[i]))
            z = jump_binary(jump(clean_text[i]))
            converted_commands.append('111'+y+x+z)
     
    '''Iterates through the converted_commands array and writes each element
    to a separate line in the given .hack output file'''
    
    with open(output_file, "w") as writing_function:
        for i in converted_commands:
            writing_function.write('%s\n' % i)
#%%        


                    
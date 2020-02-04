from Code_Writer_Module import (writeArithmetic, writePush, writePop, writeLabel,
writeLabel_in_func, write_goto, write_goto_in_func, write__if_goto, write__if_goto_in_func,
writeFunction, writeCall, writeReturn, writeCall_Sys_init, fileWriter)

from Parser_Module import open_and_clean_text, commandType
#%%   
def VMtranslator(output_file):
    
    import glob
    
    complete_asm_commands = ['@256', 'D=A', '@SP', 'M=D']
    writeCall_Sys_init(['call', 'Sys.init', '0'], complete_asm_commands)
    
    vm_file_names = []
    for vm_file in glob.glob('*.vm'):
        vm_file_names.append(vm_file)
    
    function_number = 1
    
    eq_symbol_counter = 1
    gt_symbol_counter = 1
    lt_symbol_counter = 1
    end_symbol_counter = 1
    dummy_counter = 0
    
    for i in vm_file_names:
    
        clean_text = open_and_clean_text(i)
        input_file_noext = i.split('.')[0]
        assembly_commands = []
    
        current_function = ''
        in_func_indic = 0

    
        for j in range(0, len(clean_text)): 
            parsed_command = clean_text[j].split(' ')
        
            if commandType(parsed_command) == 'C_PUSH':
                writePush(parsed_command, input_file_noext, assembly_commands)
        
            if commandType(parsed_command) == 'C_POP':
                writePop(parsed_command, input_file_noext, assembly_commands)
        
            if commandType(parsed_command) == 'C_ARITHMETIC':
                if parsed_command[0] == 'eq':
                    writeArithmetic(parsed_command, eq_symbol_counter, 
                                end_symbol_counter, assembly_commands)
                    eq_symbol_counter += 1
                    end_symbol_counter += 1
                
                if parsed_command[0] == 'gt':
                    writeArithmetic(parsed_command, gt_symbol_counter,
                                end_symbol_counter, assembly_commands)
                    gt_symbol_counter +=1
                    end_symbol_counter += 1
            
                if parsed_command[0] == 'lt':
                    writeArithmetic(parsed_command, lt_symbol_counter,
                                end_symbol_counter, assembly_commands)
                    lt_symbol_counter += 1
                    end_symbol_counter += 1
            
                if parsed_command[0] != 'eq' and parsed_command[0] != 'gt' and parsed_command[0] != 'lt':
                    writeArithmetic(parsed_command, dummy_counter,
                                dummy_counter, assembly_commands)
        
            if commandType(parsed_command) == 'C_LABEL':
                if in_func_indic == 0:
                    writeLabel(parsed_command, assembly_commands)
                else:
                    writeLabel_in_func(parsed_command, current_function,
                                   assembly_commands)
        
            if commandType(parsed_command) == 'C_GOTO':
                if in_func_indic == 0:
                    write_goto(parsed_command, assembly_commands)
                else:
                    write_goto_in_func(parsed_command, current_function, 
                                   assembly_commands)
                
            if commandType(parsed_command) == 'C_IF':
                if in_func_indic == 0:
                    write__if_goto(parsed_command, assembly_commands)
                else:
                    write__if_goto_in_func(parsed_command, current_function, 
                                       assembly_commands)
        
            if commandType(parsed_command) == 'C_FUNCTION':
                current_function = parsed_command[1]
                in_func_indic += 1
                writeFunction(parsed_command, assembly_commands)
        
            if commandType(parsed_command) == 'C_CALL':
                writeCall(parsed_command, function_number, assembly_commands)
                function_number +=1
        
            if commandType(parsed_command) == 'C_RETURN':
                writeReturn(assembly_commands)
                
        complete_asm_commands = complete_asm_commands+assembly_commands

    fileWriter(output_file, complete_asm_commands)

#%%

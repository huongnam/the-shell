from builtin import run_file
import subprocess as sub
from namtestswiththisfile import handle_input
from history import read_history_file


def dep(item, functions):
    flag = True
    type_in = handle_input(item)
    exit_code = None
    if type_in:
        command = type_in[0]
        if command in functions.keys():
            if 'history' in command:
                history_lst = read_history_file(curpath)
                flag, exit_code = process_function(functions, command,
                                        history_lst)
            else:
                flag, exit_code = process_function(functions, command,
                                                   type_in)
        else:
            exit_code = run_file(type_in)
    return flag, exit_code


def get_what_inside_the_backquotes(string):
    lst_command = []
    count = 0
    if "``" in string:
        string = string.replace("``", "")
    while "`" in string:
        for i in range(len(string)):
            if "`" in string:
                if string[i] == "`":
                    j = i
                    while string[j+1] != "`":
                        j += 1
                    lst_command.append(string[i+1:j+1])
                    string = string.replace(string[i:j+2], str(count))
                    count += 1
    return [lst_command, string.strip().split()]


# print(get_what_inside_the_backquotes("echo `echo nam` `echo tran` asdsa"))



def command_substitution(args):
    inside_backquotes = get_what_inside_the_backquotes(args)[0]
    command_line = get_what_inside_the_backquotes(args)[1]
    # print(lst_commands)
    commands_to_do = []
    for item in inside_backquotes:
    # try:
        out = sub.run(item.split(), stdout=sub.PIPE)
        out = out.stdout.decode().strip()
        print("1111"+out+"222")
        commands_to_do.append(out)
    # except Fil

    print(commands_to_do)
    if commands_to_do:
        for i in range(len(commands_to_do)):
            for j in range(len(command_line)):
                if command_line[j] == str(i):
                    command_line[j] = commands_to_do[i]
    print(command_line)
    while "" in command_line:
        for item in command_line:
            if item == "":
                command_line.remove(item)
    print(command_line)
    new_command_line = " ".join(item for item in command_line)
    print(new_command_line)
    dep(new_command_line, functions)




# ['a','b','c']
# def

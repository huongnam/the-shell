from input_excuting import input_excuting
import subprocess as sub

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


def command_substitution(args, functions):
    inside_backquotes = get_what_inside_the_backquotes(args)[0]
    command_line = get_what_inside_the_backquotes(args)[1]
    commands_to_do = []
    if args.count('`') % 2 != 0:
        print("Have you missed something?")
        return None
    if len(inside_backquotes) == 1 and inside_backquotes[0] == "pwd":
        print("intek-sh: " + environ['PWD'] + ": Is a directory")
    else:
        for item in inside_backquotes:
            # try:
            out = sub.run(item.split(), stdout=sub.PIPE)
            out = out.stdout.decode().strip()
            commands_to_do.append(out)
        if commands_to_do:
            for i in range(len(commands_to_do)):
                for j in range(len(command_line)):
                    if command_line[j] == str(i):
                        command_line[j] = commands_to_do[i]
        while "" in command_line:
            for item in command_line:
                if item == "":
                    command_line.remove(item)
        new_command_line = " ".join(item for item in command_line)
        input_excuting(new_command_line, functions)

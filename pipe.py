import os
import sys
import subprocess as sub
from re import split, compile

def get_in_path(args):
    '''
    looks for the path given in PATH variable located in /bin or /usr/bin
    and inserts to the first item in command
    ex: ['/bin/ls', '-l']
    '''
    try:
        PATH = os.environ['PATH'].split(':')
    except KeyError:
        print("intek-sh: " + args[0] + ": command not found")
        return None
    for item in PATH:
        if os.path.exists(item+'/'+args[0]):
            return [item + '/' + args[0]] + args[1:]
    print("intek-sh: " + args[0] + ": command not found")
    return None


def redirect_out(file, mode):
    #  redirects output to file
    sys.stdout = open(file, mode)
    return True


def redirect_in(file):
    #  receives input from file
    with open(file, "r") as f:
        content = f.read()
    return content.encode()


def redirect_err(file, mode):
    #  redirects error to file
    sys.stderr = open(file, mode)
    return False

def handle_redirection(command, _input, flag):
    indicators = [">", ">>", "<", "<<", "2>", "2>>"]
    lst_file = []
    commands_to_do = []
    for i in range(len(command)):
        if command[i] in indicators:
            #  the item after the indicator is the file
            file_name = command[i+1]
            #  to make sure this is not ">>"
            if command[i] == ">" and command[i-1] != ">" and command[i+1] != ">":
                flag = redirect_out(file_name, "w")
            elif command[i] == ">>":
                redirect_out(file_name, "a")
            elif command[i] == "<":
                _input = redirect_in(file_name)
            elif command[i] == "<<":
                str = ""
                loop = True
                while loop:
                    line_in = input("> ")
                    if line_in == file_name:
                        break
                    str += line_in + "\n"
                _input = str.encode()
            elif command[i] == "2>":
                redirect_err(file_name, "w")
            elif command[i] == "2>>":
                redirect_err(file_name, "a")
            lst_file.append(file_name)
    ''' returns the commands to do, without any file name or indicators
    ex: "ls -al > nam"
    -> ['/bin/ls', '-al']
    '''
    for item in command:
        if item not in lst_file and item not in indicators:
            commands_to_do.append(item)
    #  if this is the last pipe
    if flag is True:
        sub.run(commands_to_do, stdout=sys.stdout, input=_input, stderr=sys.stderr)
        return None
    child = sub.run(commands_to_do, stdout=sub.PIPE, input=_input, stderr=sys.stderr)
    return child.stdout


def handle_pipe(args):
    indicators = [">", ">>", "<", "<<", "2>", "2>>"]
    #  split the indicators in case the user gives no spaces between them
    pattern = "(>>?|<<?)"
    args = split(pattern, args)
    new_args = " ".join(item for item in args)
    #  returns a list of pipes
    commands = new_args.split("|")
    temp_pipe = None
    #  stores the original sys.stdout, sys.stdin, sys.stderr
    _out, _in, _err = sys.stdout, sys.stdin, sys.stderr
    '''
    !!! special case: ls | grep n > nam
    if there's no file nam listed in nam, it's wrong
    so I create the file first (its priority is higher than that of the pipe)
    '''
    for item in commands:
        item = item.split()
        for i in range(len(item)):
            if item[i] == ">":
                if item[i-1] != ">" and item[i+1] != ">":
                    new_file = open(item[i+1], "w")
    for i in range(len(commands)):
        # cho nay can globbing, path exansion nua
        command = commands[i].split()
        command = get_in_path(command)
        if command is None:
            break
        #  if i == len(commands) - 1, this is the final pipe to do
        temp_pipe = handle_redirection(command, temp_pipe, i==len(commands)-1)
        #  receives the original sys.stdout, sys.stdin, sys.stderr stored before
        sys.stdout, sys.stdin, sys.stderr = _out, _in, _err

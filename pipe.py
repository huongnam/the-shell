from builtin import run_file
import os
import sys
import subprocess as sub

def tai_Tran_moi_co_ham_nay(args):
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


def handle_redirection(command, _input, flag):
    indicators = [">", ">>", "<", "<<", "2>"]
    dict_out = {">": "w", ">>": "a"}
    dict_err = {"2>": "w", "2>>": "a"}
    filename = []
    commands_to_do = []
    for i in range(len(command)):
        if command[i] in indicators:
            if command[i] in dict_out:
                sys.stdout = open(command[i + 1], dict_out[command[i]])
                flag = True
            elif command[i] == "<":
                f = open(command[i + 1], "r")
                _input = f.read()
                f.close()
            elif command[i] in dict_err:
                sys.stderr = open(command[i + 1], dict_err[command[i]])
            filename.append(command[i+1])
    for item in command:
        if item not in filename:
            if item not in indicators:
                commands_to_do.append(item)
    print(commands_to_do)
    if flag is True:
        sub.run(commands_to_do, stdout=sys.stdout, input=_input, stderr=sys.stderr)
        return None
    child = sub.run(commands_to_do, stdout=sub.PIPE, input=_input, stderr=sys.stderr)
    return child.stdout


def handle_pipe(args):
    commands = args.split("|")
    temp_pipe = None
    _out, _in, _err = sys.stdout, sys.stdin, sys.stderr
    for i in range(len(commands)):
        # cho nay can globbing, path exansion nua
        command = commands[i].split()
        command = tai_Tran_moi_co_ham_nay(command)
        # if not command:
        #     break
        len_command = len(commands) - 1

        temp_pipe = handle_redirection(command, temp_pipe, len_command == i)
        sys.stdout, sys.stdin, sys.stderr = _out, _in, _err

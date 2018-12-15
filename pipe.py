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


def redirect_out(file, mode):
    sys.stdout = open(file, mode)
    return True


def redirect_in(file):
    with open(file, "r") as f:
        content = f.read()
    return content.encode()


def redirect_err(file, mode):
    sys.stderr = open(file, mode)
    return False

def handle_redirection(command, _input, flag):
    indicators = [">", ">>", "<", "<<", "2>"]
    lst_file = []
    commands_to_do = []
    for i in range(len(command)):
        if command[i] in indicators:
            file_name = command[i+1]
            if command[i] is ">":
                redirect_out(file_name, "w")
            elif command[i] is ">>":
                redirect_out(file_name, "a")
            elif command[i] is "<":
                _input = redirect_in(file_name)
            elif command[i] is "<<":
                str = ""
                print("gra")
                while True:
                    line_in = input("> ")
                    if line_in == file_name:
                        break
                    str += line_in + "\n"
                _input = str.encode()

            elif command[i] == "2>":
                redirect_err(file_name, "w")
            elif command[i] == "2>>":
                redirect_err(file_name, "r")
            lst_file.append(file_name)
    for item in command:
        if item not in lst_file and item not in indicators:
            commands_to_do.append(item)
    if flag is True:
        sub.run(commands_to_do, stdout=sys.stdout, input=_input, stderr=sys.stderr)
        return None
    child = sub.run(commands_to_do, stdout=sub.PIPE, input=_input, stderr=sys.stderr)
    return child.stdout


def handle_pipe(args):
    commands = args.split("|")
    temp_pipe = None
    _out, _in, _err = sys.stdout, sys.stdin, sys.stderr
    for item in commands:
        # item.strip()
        item = item.split()
        for i in range(len(item)):
            if item[i] is ">":
                print(item)
                print("ho")
                new_file = open(item[i+1], "w")
    for i in range(len(commands)):
        # cho nay can globbing, path exansion nua
        command = commands[i].split()
        command = tai_Tran_moi_co_ham_nay(command)
        if command is None:
            break

        temp_pipe = handle_redirection(command, temp_pipe, i==len(commands)-1)
        sys.stdout, sys.stdin, sys.stderr = _out, _in, _err

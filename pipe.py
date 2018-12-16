# from builtin import run_file
import os
import sys
import subprocess as sub
from re import split, compile

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
    indicators = [">", ">>", "<", "<<", "2>", "2>>"]
    lst_file = []

    commands_to_do = []
    for i in range(len(command)):
        if command[i] in indicators:
            file_name = command[i+1]

            if command[i] == ">" and command[i-1] != ">" and command[i+1] != ">":
                print("co vo day k")
                flag = redirect_out(file_name, "w")
                # print(flag)
            elif command[i] == ">>":
                print("hay la vo day")
                redirect_out(file_name, "a")
            elif command[i] == "<":
                _input = redirect_in(file_name)
            elif command[i] == "<<":
                str = ""
                print("gra")
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
            else:
                print("chac la zo day")
            lst_file.append(file_name)
            # print(lst_file)
            # print("111" + file_name + "222")

    for item in command:
        if item not in lst_file and item not in indicators:
            commands_to_do.append(item)
    print(commands_to_do)
    if flag is True:
        sub.run(commands_to_do, stdout=sys.stdout, input=_input, stderr=sys.stderr)
        return None
    child = sub.run(commands_to_do, stdout=sub.PIPE, input=_input, stderr=sys.stderr)
    return child.stdout


def handle_pipe(args):
    print(args)
    indicators = [">", ">>", "<", "<<", "2>", "2>>"]
    # pattern = "(<<?\s?\w?|\d?>>?\s?\w?)"
    # pattern = "(\d?>>?|<<?\d?)"
    # args = split(pattern, args)
    pattern = ('(.*)(<<*)(.*)(>>*)(.*)')
    print(split(pattern, args))
    # print(args)
    new_args = " ".join(item for item in args)
    # print(args)
    # new_args = []
    # args = args.split()
    # #
    # for i in range(len(args)):
    #     if ">" in args[i] or "<" in args[i]:
    #         # while ">" in args[i] or "<" in args[i]:
    #         for j in range(len(args[i])):
    #             try:
    #                 if args[i][j] in indicators:
    #                     if j == 1 and args[i][0] in "1234567890":
    #                         print("hoho")
    #                         if args[i][2] == args[i][j]:
    #                             print("vo day")
    #                             new_args.append(args[i][:3])
    #                             args[i] = args[i].replace(args[i][:3], "", 1)
    #                         else:
    #                             print("hay la vo day")
    #                             new_args.append(args[i][:2])
    #                             args[i] = args[i].replace(args[i][:2], "", 1)
    #
    #                     else:
    #                         print(args[i])
    #                         print("to")
    #                         if args[i][j+1] == args[i][j]:
    #                             new_args.append(args[i][:j])
    #
    #                             new_args.append(args[i][j:j+2])
    #                             args[i] = args[i].replace(args[i][:j+2], "", 1)
    #                             print(args[i])
    #                         else:
    #                             print("di vo day")
    #             except IndexError:
    #                 pass
    #     else:
    #         new_args.append(args[i])

#
# if "``" in string:
#     string = string.replace("``", "")
# while "`" in string:
#     for i in range(len(string)):
#         if "`" in string:
#             if string[i] == "`":
#                 j = i
#                 while string[j+1] != "`":
#                     j += 1
#                 lst_command.append(string[i+1:j+1])
#                 string = string.replace(string[i:j+2], str(count))
#                 count += 1
# return [lst_command, string.strip().split()]

    #
    # print(new_args)
    #
    # #         if args[i - 1] is not " " or args[i + 1] is not " ":
    # #             new_str = " " + args[i] + " "
    # #             args = args.replace(args[i], new_str)
    # # args
    # print(args)
    commands = new_args.split("|")
    temp_pipe = None
    _out, _in, _err = sys.stdout, sys.stdin, sys.stderr
    for item in commands:
        # item.strip()
        item = item.split()
        for i in range(len(item)):
            if item[i] == ">":
                print("ha")
                if item[i-1] != ">" and item[i+1] != ">":
                # print(item)
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

#!/usr/bin/env python3
from readline import parse_and_bind, set_completer, set_completer_delims
from dynamic import make_subcommand_completer
from os import environ, listdir
import builtins_package.process_cd
import builtins_package.process_exit
import builtins_package.process_export
import builtins_package.process_printenv
import builtins_package.process_run_file
import builtins_package.process_unset


'''
cd      : change directory
printenv: print all or part of environment
export  : mark each name to be passed to child processes in the environment
unset   : remove each variable or function name
exit    : end process
'''


def process_function(functions, command, args):
    exit_code = functions[command](args)
    if 'exit' in command:
        return False, exit_code
    else:
        return True, exit_code


def handle_input(_args, exit_code):
    type_in = []
    replace_things = []
    _args = _args.split()
    for element in _args:
        if element:
            type_in.append(element)
    if replace_things:
        type_in += replace_things
    return type_in


def get_all_cmds():
    if 'PATH' in environ.keys():
        for cmd_path in environ['PATH'].split(':'):
            try:
                cmds = listdir(cmd_path)
            except FileNotFoundError:
                continue
            for cmd in cmds:
                commands.add(cmd)


def main():
    global type_in
    global exit_code
    global commands
    exit_code = 0
    flag = True
    commands = {'history', 'cd', 'printenv', 'export', 'unset', 'exit'}
    functions = {
            'cd': builtins_package.process_cd.cd,
            'printenv': builtins_package.process_printenv.printenv,
            'export': builtins_package.process_export.export,
            'unset': builtins_package.process_unset.unset,
            'exit': builtins_package.process_exit.sh_exit,
            'history': '_'
            }
    while flag:
        # get all the command in environment PATH
        get_all_cmds()

        parse_and_bind('tab: complete')
        set_completer(make_subcommand_completer(commands))
        set_completer_delims(" \t")
        _args = input('\033[92m\033[1mintek-sh$\033[0m ')
        type_in = handle_input(_args, exit_code)
        if type_in:
            command = type_in[0]
            if command in functions.keys():
                flag, exit_code = process_function(functions, command, type_in)
            else:
                exit_code = builtins_package.process_run_file.run_file(type_in)


if __name__ == '__main__':
    main()

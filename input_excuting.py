from history import read_history_file
from builtins_package.process_run_file import run_file
from exit_status import get_exit_status


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
            # exit status
            if '$?' in element or '${?}' in element:
                replace_things = get_exit_status(element, str(exit_code))
            else:
                type_in.append(element)
    if replace_things:
        type_in += replace_things
    return type_in


def input_excuting(item, functions):
    flag = True
    exit_code = 0
    type_in = handle_input(item, exit_code)

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

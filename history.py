'''
Event Designators
     An event designator is a reference to a command line entry in
     the history list.  Unless the reference is absolute, events are rela‐
     tive to the current position in the history list.

     !      Start a history substitution, except when followed by a blank,
            newline, = or (.
     !n     Refer to command line n.
     !-n    Refer to the current command minus n.
     !!     Refer to the previous command.  This is a synonym for `!-1'.
     !string
            Refer to the most recent command preceding the current position
            in the history list starting with string.
     !?string[?]
            Refer  to  the most recent command preceding the current position
            in the history list containing string.  The trailing ? may
            be omitted if string is followed immediately by a newline.
     ^string1^string2^
            Quick substitution.  Repeat the last command, replacing string1
            with string2.  Equivalent to ``!!:s/string1/string2/''
     !#     The entire command line typed so far.
'''


def write_history_file(args, curpath):
    history_file = open(curpath + '/.intek-sh_history', 'a')
    history_file.write(args + '\n')
    history_file.close()


def expand_history_file(_args, special_cases, curpath, history_lst):
    written = False
    if not _args.startswith('!') and _args not in special_cases and\
        not _args.startswith(' '):
        if history_lst:
            if _args != history_lst[-1].strip('\n'):
                if '!#' not in _args and '^' not in _args:
                    write_history_file(_args, curpath)
                    written = True
        else:
            if '!#' not in _args and '^' not in _args:
                write_history_file(_args, curpath)
                written = True
    return written


def read_history_file(curpath):
    try:
        history_file = open(curpath + '/.intek-sh_history', 'r')
    except FileNotFoundError:
        return None
    history_lst = history_file.readlines()
    history_file.close()
    return history_lst


def print_history(history_lst):
    for index, element in enumerate(history_lst):
        # justify columns
        element = element.strip('\n')
        # right justify the numbers
        _order = str(index+1).rjust(len(str(len(history_lst))), ' ')
        # left justify the commands
        command = element.ljust(len(max(history_lst, key=len)), ' ')
        print(' ' * 4 + _order + '  ' + command)
    return 0


# replace args as cmd and print it
def print_args(args, cmd):
    args = cmd
    print(args)
    return args.strip('\n'), True


def handle_special_case(exist, args):
    continue_flag = False
    if args.startswith('!'):
        # no matched event in history_lst
        if not exist:
            if sub_failed2:
                continue_flag = True
            else:
                print('intek-sh: ' + args + ': event not found')
                continue_flag = True
        else:  # match event in history_lst but
            # command starts with ! and followed by a blank space
            if len(args) is 1 or args == '! ':
                continue_flag = True
    # substitution errors
    elif args.startswith('^') and sub_failed:
        continue_flag = True
    # out of capability
    elif alert:
        continue_flag = True
    return continue_flag, args


def handle_emotion_prefix(args, history_lst):
    global sub_failed2
    exist = False
    sub_failed2 = False
    # command type: '!?'
    if args[1:].startswith('?'):
        args = args.strip('!?')
        # traverse through history_lst in reversed order
        for cmd in reversed(history_lst):
            # if cmd has args -> take the cmd and break the loop
            if args in cmd:
                args, exist = print_args(args, cmd.strip('\n'))
                break

    # command type: '!!'
    elif args[1:].startswith('!'):
        temp = history_lst[len(history_lst) - 1].strip('\n')
        new_args = args.replace('!!', temp)
        # command type: '!!:s/string1/string2/'
        if ':' in args[1:]:
            if 's/' in args[1:]:
                # command is !!:s/s1 -> pop s1 out of string
                if args.count('/') is 1:
                    temp_lst = []
                    for w in temp:
                        temp_lst.append(w)
                    if args[5:] in temp_lst:
                        temp_lst.remove(args[5:])
                        new_args = ''.join(temp_lst)
                        args, exist = print_args(args, new_args)
                    else:  # if p not in string -> raise error
                        print('intek-sh: :s' + args + ': substitution failed')
                        sub_failed2 = True
                # command has both s1 and s2 -> replace s1 with s2
                else:
                    arg_lst = args[1:].strip('/').split('/')
                    pos = new_args.find(':')
                    new_args = new_args[:pos].replace(arg_lst[-2], arg_lst[-1])
                    args, exist = print_args(args, new_args)
            else:  # command doesn't follow the format
                print('intek-sh: ' + args[2:] + ': substitution failed')
                sub_failed2 = True
        else:
            args, exist = print_args(args, new_args)

    # command type: '!n'
    elif args[1].isdigit():
        prefix = ''
        # get the prefix (n)
        for word in args[1:]:
            if word.isdigit():
                prefix += word
            else:
                break
        number = int(prefix)
        if (number-1) < len(history_lst):
            new_args = args.replace('!' + prefix, history_lst[number-1])
            args, exist = print_args(args, new_args.strip('\n'))

    # command type: '!-n'
    elif args[1] is '-' and args[2].isdigit():
        prefix = ''
        for word in args[2:]:
            if word.isdigit():
                prefix += word
            else:
                break
        number = int(prefix)
        if number < len(history_lst):
            new_args = args.replace('!' + '-' + prefix,
                                    history_lst[len(history_lst) - number])
            args, exist = print_args(args, new_args.strip('\n'))

    # command starts with '!string'
    elif args[1].isalpha():
        # command type: '!string randomstring'
        if ' ' in args:
            args_lst = args.split(' ')
            for cmd in reversed(history_lst):
                if cmd.startswith(args[1]):
                    args_lst.pop(0)
                    args_lst.insert(0, cmd.strip('\n'))
                    args, exist = print_args(args, ' '.join(args_lst))
                    break
        else:  # command type: '!string'
            for cmd in reversed(history_lst):
                if cmd.startswith(args[1:]):
                    args, exist = print_args(args, cmd.strip('\n'))
                    break
    return args, exist


def handle_caret(args, history_lst):
    global sub_failed
    sub_failed = False
    exist = False
    new_args = ''
    temp = history_lst[len(history_lst) - 1].strip('\n')
    # command is ^s -> pop s out of string
    if args.count('^') is 1:
        temp_lst = []
        for w in temp:
            temp_lst.append(w)
        if args[1:] in temp_lst:
            temp_lst.remove(args[1:])
            new_args = ''.join(temp_lst)
            args, exist = print_args(args, new_args)
        else:
            print('intek-sh: :s' + args + ': substitution failed')
            sub_failed = True
    else:  # command type: ^string1^string2 -> replace string1 with string2
        args_lst = args.strip('^').split('^')
        if args_lst[0] in temp:
            new_args = temp.replace(args_lst[0], args_lst[-1])
            args, exist = print_args(args, new_args)
        else:
            print('intek-sh: :s' + args + ': substitution failed')
            sub_failed = True
    return args, exist


def handle_command(args, history_lst):
    global sub_failed
    global alert
    alert = False
    exist = False
    if args.startswith('!'):
        if len(args) is 1 or args[1] is ' ' or args[1] is '=':
            return args, True
        elif args[1] is '(':
            return args[0], exist
        elif args[1] is '#':
            return args, True
        else:
            args, exist = handle_emotion_prefix(args, history_lst)
    # command type: '^string1^string2^'
    elif args.startswith('^'):
        args, exist = handle_caret(args, history_lst)
    elif '!#' in args:
        print('intek-sh: sorry this is out of my capability')
        alert = True
    return args, exist

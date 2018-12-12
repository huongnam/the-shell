def write_history_file(args, curpath):
    history_file = open(curpath + '/.intek-sh_history', 'a')
    history_file.write(args + '\n')
    history_file.close()


def read_history_file(curpath):
    history_file = open(curpath + '/.intek-sh_history', 'r')
    history_lst = history_file.readlines()
    history_file.close()
    return history_lst


def expand_history_file(_args, special_cases, curpath):
    written = False
    if not _args.startswith('!') and _args not in special_cases:
        if '!#' not in _args and '^' not in _args:
            write_history_file(_args, curpath)
            written = True
    return written


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
    if args.startswith('!'):
        # no matched event in history_lst
        if not exist:
            if sub_failed2:
                raise ValueError
            else:
                print('intek-sh: ' + args + ': event not found')
                raise ValueError
        else:  # match event in history_lst but
            # command starts with ! and followed by a blank space
            if len(args) is 1 or args == '! ':
                raise ValueError
            # command starts with '!=' -> command not found
            elif args[1] is '=':
                raise Exception
            # command type: ! with multiple spaces and random string
            elif len(args) > 2:
                args = args.strip('!').strip(' ')
                raise Exception
    # substitution errors
    elif args.startswith('^') and sub_failed:
        raise ValueError
    # out of capability
    elif alert:
        raise ValueError
    return args


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

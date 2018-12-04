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


def write_history_file(args):
    history_file = open('.intek-sh_history', 'a')
    history_file.write(args + '\n')
    history_file.close()


def read_history_file():
    history_file = open('.intek-sh_history', 'r')
    history_lst = history_file.readlines()
    history_file.close()
    return history_lst


def print_history(history_lst):
    for index, element in enumerate(history_lst):
        # justify columns
        element = element.strip('\n')
        _order = str(index+1).rjust(len(str(len(history_lst))), ' ')
        command = element.ljust(len(max(history_lst, key=len)), ' ')
        print(' ' * 4 + _order + '  ' + command)


# replace args as cmd and print it
def print_args(args, cmd):
    args = cmd
    print(args)
    return args.strip('\n'), True


# handle special case of '!'
def handle_special_case(exist, args):
    continue_flag = False
    pass_flag = False
    if args.startswith('!'):
        # no matched event in history_lst
        if not exist:
            if sub_failed2:
                continue_flag = True
            else:
                print('intek-sh: ' + args + ': event not found')
                continue_flag = True
        else:
            # command starts with ! and followed by a blank space
            if len(args) is 1 or args == '! ':
                continue_flag = True
            # command starts with '!=' -> command not found
            elif args[1] is '=':
                pass_flag = True
            elif len(args) > 2:
                pass_flag = True
    elif args.startswith('^') and sub_failed:
        continue_flag = True
    elif alert:
        continue_flag = True
    return continue_flag, pass_flag


def handle_emotion_prefix(args, history_lst):
    global sub_failed2
    exist = False
    sub_failed2 = False
    # command type: '!?'
    if args[1:].startswith('?'):
        args = args.strip('!?')
        for cmd in reversed(history_lst):
            if args in cmd:
                args, exist = print_args(args, cmd)
                break

    # command type: '!!'
    elif args[1:].startswith('!'):
        temp = history_lst[len(history_lst) - 1].strip('\n')
        new_args = args.replace('!!', temp)
        # command type: '!!:s/string1/string2/'
        if ':' in args[1:]:
            if 's/' in args[1:]:
                arg_lst = args[1:].strip('/').split('/')
                new_args = new_args[:new_args.find(':')].replace(arg_lst[-2],
                                                                 arg_lst[-1])
                args, exist = print_args(args, new_args)
                write_history_file(args)
            else:
                print('intek-sh: ' + args[2:] + ': substitution failed')
                sub_failed2 = True
        else:
            args, exist = print_args(args, new_args)
            write_history_file(args)

    # command type: '!n'
    elif args[1].isdigit():
        prefix = ''
        for word in args[1:]:
            if word.isdigit():
                prefix += word
            else:
                break
        number = int(prefix)
        if (number-1) < len(history_lst):
            new_args = args.replace('!' + prefix, history_lst[number-1])
            args, exist = print_args(args, new_args)

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
            args, exist = print_args(args, new_args)

    # command type: '!string'
    elif args[1].isalpha():
        if ' ' in args:
            args_lst = args.split(' ')
            for cmd in reversed(history_lst):
                if cmd.startswith(args[1]):
                    args_lst.pop(0)
                    args_lst.insert(0, cmd.strip('\n'))
                    args, exist = print_args(args, ' '.join(args_lst))
                    break
        else:
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
            write_history_file(args)
        else:
            print('intek-sh: :s' + args + ': substitution failed')
            sub_failed = True
    else:  # command type: ^string1^string2 -> replace string1 with string2
        args_lst = args.strip('^').split('^')
        if args_lst[0] in temp:
            new_args = temp.replace(args_lst[0], args_lst[-1])
            args, exist = print_args(args, new_args)
            write_history_file(args)
        else:
            print('intek-sh: :s' + args + ': substitution failed')
            sub_failed = True
    return args, exist


def handle_command(args, history_lst):
    global sub_failed
    global alert
    alert = False
    exist = False
    hashtag = False
    if args.startswith('!'):
        if len(args) is 1 or args[1] is ' ' or args[1] is '=':
            return args, True, hashtag
        elif args[1] is '(':
            return args[0], exist, hashtag
        elif args[1] is '#':
            return args, True, hashtag
        else:
            args, exist = handle_emotion_prefix(args, history_lst)
    # command type: '^string1^string2^'
    elif args.startswith('^'):
        args, exist = handle_caret(args, history_lst)
    elif '!#' in args:
        print('intek-sh: sorry this is out of my capability')
        alert = True
    return args, exist, hashtag

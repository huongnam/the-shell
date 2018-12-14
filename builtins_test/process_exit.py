from sys import exit


# check if args is more than 1
def check_args(args):
    if len(args) is not 1:
        return True
    else:
        return False


def sh_exit(exit_args):
    if check_args(exit_args):
        if exit_args[1].isdigit():
            print('exit ' + ' '.join(exit_args[1:]))
            exit_code = int(' '.join(exit_args[1:]))
        else:
            print('exit\nintek-sh: exit: ' + ' '.join(exit_args[1:]))
            exit_code = 0
    else:
        print('exit')
        exit_code = 0
    exit(exit_code)

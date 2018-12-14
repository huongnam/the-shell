from os import chdir, environ, getcwd, path


def print_error(arg, _error, _cd=''):
    return "intek-sh: " + _cd + arg + _error


# change the path and set environ PWD as the path
def change_dir(dir_path):
    chdir(dir_path)
    environ['PWD'] = getcwd()


# check if args is more than 1
def check_args(args):
    if len(args) is not 1:
        return True
    else:
        return False


def cd(cd_args):
    _path = None
    # if args is more than 1 -> path is the last argument
    if check_args(cd_args):
        _path = cd_args[1]
    if _path:
        if _path is '..':
            change_dir('..')
            exit_code = 0
        else:
            try:
                change_dir(path.abspath(_path))
                exit_code = 0
            except FileNotFoundError:
                print(print_error(_path + ': ', "No such file or"
                      " directory", "cd: "))
                exit_code = 1
    else:  # if len path is 1 -> jump to HOME
        if 'HOME' in environ:
            change_dir(environ['HOME'])
            exit_code = 0
        else:
            print(print_error("", "HOME not set", "cd: "))
            exit_code = 1
    return exit_code

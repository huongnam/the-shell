#!/usr/bin/env python3
def history(history_lst):
    for index, element in enumerate(history_lst):
        # justify columns
        _order = str(index+1).rjust(len(str(len(history_lst))), ' ')
        command = element.ljust(len(max(history_lst, key=len)), ' ')
        print(' ' + _order + '  ' + command)

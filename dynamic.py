from glob import glob
import readline
from os import path


def list_dir_for_cd(text):
    cd_matches = []
    for filename in glob(text + '*'):
        if path.isdir(filename):
            cd_matches.append(filename + '/ ')
    # including hidden files and folders
    for hidden_filename in glob(text + '.*'):
        if path.isdir(hidden_filename):
            cd_matches.append(hidden_filename + '/ ')
    return cd_matches


def list_dir_for_anythingElse(text):
    anythingElse_matches = []
    for filename in glob(text + '*'):
        if path.isdir(filename):
            anythingElse_matches.append(filename + '/ ')
        else:
            anythingElse_matches.append(filename + ' ')
    # including hidden files and folders
    for hidden_filename in glob(text + '.*'):
        if path.isdir(hidden_filename):
            anythingElse_matches.append(hidden_filename + '/ ')
        else:
            anythingElse_matches.append(hidden_filename + ' ')
    return anythingElse_matches


def make_subcommand_completer(commands):
    def custom_complete(text, state):
        matches = []
        ''' Simplistic parsing of the command-line so far. We want to know
         if the user is still entering the command, or if the command is
         already there and now we have to complete the subcommand. '''
        linebuf = readline.get_line_buffer()
        parts = linebuf.split()

        if len(parts) >= 1 and linebuf.endswith(' '):
            ''' If we're past the first part and there is whitespace at
            the end of the buffer, it means we're already completing the
            next part. '''
            parts.append('')

        if len(parts) is 0:
            ''' do nothing when the user doesn't enter anything '''
            matches.append(None)
            return matches[state]

        elif len(parts) is 1:
            ''' If the completion happens on the first word,
                commands are suggested'''
            for key in commands:
                if key.startswith(text):
                    matches.append(key + ' ')
            matches.append(None)
            return matches[state]

        elif len(parts) >= 2:
            ''' otherwise files in the current directly are suggested.'''
            command = parts[0]

            if command == 'cd':
                ''' just list the present directories if command is cd '''
                matches = list_dir_for_cd(text)
                matches.append(None)

            else:
                ''' Treat 'file' specially, by looking for matching files
                in the current directory.'''
                matches = list_dir_for_anythingElse(text)
                matches.append(None)
            return matches[state]
    return custom_complete

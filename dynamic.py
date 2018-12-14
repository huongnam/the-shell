from glob import glob
import readline
from os import path, listdir


def make_subcommand_completer(commands):
    def custom_complete(text, state):
        matches = []
        ''' Simplistic parsing of the command-line so far. We want to know if the
         user is still entering the command, or if the command is already there
         and now we have to complete the subcommand. '''
        linebuf = readline.get_line_buffer()
        parts = linebuf.split()

        if len(parts) >= 1 and linebuf.endswith(' '):
            ''' If we're past the first part and there is whitespace at the end of
            the buffer, it means we're already completing the next part. '''
            parts.append('')

        if len(parts) is 0:
            ''' do nothing when the user doesn't enter anything '''
            matches.append(None)
            return matches[state]

        if len(parts) is 1:
            for key in commands:
                if key.startswith(text):
                    matches.append(key + ' ')
            matches.append(None)
            return matches[state]

        elif len(parts) >= 2:
            command = parts[0]

            if command == 'cd':
                for j in glob(text + '*'):
                    if path.isdir(j):
                        matches.append(j + '/ ')
                for z in glob(text + '.*'):
                    if path.isdir(z):
                        matches.append(z + '/ ')
                matches.append(None)

            else:
                ''' Treat 'file' specially, by looking for matching files in the
                current directory.'''
                for w in glob(text + '*'):
                    if path.isdir(w):
                        matches.append(w + '/ ')
                    else:
                        matches.append(w + ' ')
                # including hidden files and folders
                for i in glob(text + '.*'):
                    if path.isdir(i):
                        matches.append(i + '/ ')
                    else:
                        matches.append(i + ' ')
                matches.append(None)
            return matches[state]
    return custom_complete

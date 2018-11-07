import hash_phrase
from getpass import getpass
import argparse
import clipboard


parser = argparse.ArgumentParser()
parser.add_argument(
    '-c',
    '--clipboard',
    help='Copy password to clipboard rather than displaying it on screen',
    action='store_true'
)
parser.add_argument(
    '-n',
    '--use-numbers',
    help='Use numbers in generated passwords',
    action='store_true'
)
parser.add_argument(
    '--separator',
    help='Separator between the words in the generated password (default: none)',  # NOQA
    default='-'
)
parser.add_argument(
    '--no-capitalize',
    help='Don`\t capitalize the words in the password',
    action='store_true'
)
parser.add_argument(
    '-e',
    '--minimum-entropy',
    help='Minimum entropy for generated passphrase. Doesn\'t reflect actual password\'s entropy.',  # NOQA
    default=90,
)
args = parser.parse_args()


# https://stackoverflow.com/questions/12586601/remove-last-stdout-line-in-python
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


if __name__ == '__main__':
    passphrase = getpass('Enter pass phrase (no characters will be shown): ')
    host = input('Enter hostname or sitename: ')
    login = input('Enter login: ')
    modifier = input('Enter modifier (optional): ')

    hash = hash_phrase.hash_phrase(
        passphrase + host + login + modifier,
        minimum_entropy=args.minimum_entropy,
        separator=args.separator,
        use_numbers=args.use_numbers,
        capitalize= not args.no_capitalize,
    )
    if args.clipboard:
        clipboard.copy(hash)
        print('Password was copied to clipboard!')
    else:
        print(hash)
        input('Copy the password and press any key to finish: \n')
        # Basic security: remove password from screen
        print(CURSOR_UP_ONE * 3 + ERASE_LINE)

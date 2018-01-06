#!/user/bin/env python3 -tt
"""
jenkinsmon documentation.
"""

import sys


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--flags options] [inputs] ')
        sys.exit(1)


# Main body
if __name__ == '__main__':
    main()

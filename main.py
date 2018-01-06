#!/user/bin/env python3 -tt
"""
jenkinsmon documentation.
"""

import sys
import yaml
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", action="store",
                    dest="config",
                    default="config.yaml",
                    help="configuration file to use")
parser.parse_args()


class InvalidConfigError(RuntimeError):

    def __init__(self, path, details):
        self.path = path
        self.details = details
        super().__init__(path, details)

    def __str__(self):
        return f"{self.path}: {self.details}"


def load_config(file):
        try:
            return yaml.load(open(file, 'r'))
        except yaml.YAMLError:
            raise InvalidConfigError(file, "invalid YAML syntax")
        except FileNotFoundError as e:
            raise InvalidConfigError(file, "not found")


def main():
    args_init = parser.parse_args()

    try:
        config = load_config(args_init.config)
    except InvalidConfigError as e:
        sys.exit(e)

    print(config)


# Main body
if __name__ == '__main__':
    main()

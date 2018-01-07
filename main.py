#!/user/bin/env python3 -tt
"""
jenkinsmon documentation.
"""

import sys
import yaml
import jenkins
import argparse
import urllib


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


class Configuration():

    def load(config_file):
            try:
                return yaml.load(open(config_file, 'r'))
            except yaml.YAMLError:
                raise InvalidConfigError(config_file, "invalid YAML syntax")
            except FileNotFoundError as e:
                raise InvalidConfigError(config_file, "not found")


def main():
    args = parser.parse_args()

    try:
        config = Configuration.load(args.config)
    except InvalidConfigError as e:
        sys.exit(e)

    servers = []
    for server in config["servers"]:
        try:
            client = jenkins.Jenkins(server["url"])
            if client.get_version():
                servers.append(client)
            else:
                continue
        except urllib.error.URLError:
            print("Communication failure with {0}".format(client.server))


# Main body
if __name__ == '__main__':
    main()

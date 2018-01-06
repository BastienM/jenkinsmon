#!/user/bin/env python3 -tt
"""
jenkinsmon documentation.
"""

import sys
import yaml
import argparse
import urllib.request


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


class Server(RuntimeError):

    def __init__(self, name, url):
        self.name = name
        self.url = url
        super().__init__(name, url)

    def getStatus(self):
        try:
            if urllib.request.urlopen(self.url).getcode() == 200:
                return True
            else:
                return False
        except urllib.error.URLError:
            print("Unable to find {0} ({1}).".format(self.name, self.url))


def main():
    args = parser.parse_args()

    try:
        config = Configuration.load(args.config)
    except InvalidConfigError as e:
        sys.exit(e)

    servers = []
    for server in config["servers"]:
        item = Server(server["name"], server["url"])
        if item.getStatus():
            servers.append(item)
        else:
            continue

    print(servers)


# Main body
if __name__ == '__main__':
    main()

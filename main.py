#!/user/bin/env python3 -tt
"""
jenkinsmon documentation.
"""

import sys
import yaml
import urllib
import jenkins
import argparse

from tabulate import tabulate
from urllib.parse import urlsplit
from colorama import Back, Style


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


def get_domain_from_uri(uri):
    return print("{0.netloc}/".format(urlsplit(uri)))


def set_print_color(status):
    color = ""
    if "anime" in status:
        color = Back.GREEN
        status = "building"

    if status == "red":
        color = Back.BLUE
        status = "failed"

    if status == "aborted":
        color = Back.MAGENTA
        status = "cancelled"

    if status == "blue":
        color = Back.BLUE
        status = "success"

    if status == "yellow":
        color = Back.YELLOW
        status = "unstable"

    if status == "disabled":
        color = Back.BLACK

    return color + " {0} ".format(status).upper() + Style.RESET_ALL


def get_jobs_list(servers):
    jobs = []
    for server in servers:
        try:
            all_jobs = server.get_jobs()
            for job in all_jobs:
                job.pop("_class", None)
                job.pop("fullname", None)
                job["name"] = "\033[1m{0}\033[0;0m".format(job["name"])
                job["color"] = set_print_color(job["color"])

                jobs.append(job)

        except jenkins.BadHTTPException:
            print("An error occured while communication with {0}".format(
                server.server))

    headers = {'name': 'Name', 'url': 'URL', 'color': 'Status'}
    print(tabulate(jobs, headers, showindex="always"))


def get_servers_info(servers):
    print("The following configured servers are available :")
    for server in servers:
        print("\t - {0} ({1})".format(server.server, server.get_version()))


def get_job_info(servers, name):
    for server in servers:
        try:
            print(server.get_job_info(name))
        except jenkins.NotFoundException:
            return print("Could not find job {0}".format(name))


def Main(args):
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

    if args.action == "servers":
        get_servers_info(servers)

    if args.action == "list":
        get_jobs_list(servers)


# Main body
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", metavar='file.yaml',
                        action="store",
                        dest="config",
                        default="config.yaml",
                        help="configuration file to use")

    parser.add_argument("action", nargs="?",
                        help="list | servers")

    args = parser.parse_args()
    Main(args)

#!/usr/bin/env python3
from zenerator.configuration import ConfigurationManager
import argparse

def start(args):
    # main or default args parsing
    print(args)

def config_flags(sub):
    manager = ConfigurationManager()
    # Config application descriptor.
    config_parser = sub.add_parser("config", help=ConfigurationManager.__doc__)
    # Display section from local.ini file.
    config_parser.add_argument(
        "-l",
        "--list",
        help=manager.list_entry.__doc__,
        nargs='?',
        default=None
        )
    config_parser.add_argument(
        "-d",
        "--dry-run",
        help="Run modifications without saving the configuration to hard disk.",
        action="store_true",
        default=False
        )
    config_parser.add_argument(
        "-v",
        "--value",
        help="The value to be modified. Only used with '--add' and '--update'.",
        type=str,
        default=None
        )
    #
    config_modifier = config_parser.add_mutually_exclusive_group()
    config_modifier.add_argument(
        "-a",
        "--add",
        help=manager.add_entry.__doc__,
        nargs='+',
        default=None
        )
    config_modifier.add_argument(
        "-r",
        "--remove",
        help=manager.remove_entry.__doc__,
        nargs='+',
        default=None
        )
    config_modifier.add_argument(
        "-u",
        "--update",
        help=manager.update_entry.__doc__,
        nargs='+',
        default=None
        )
    # Set the function to run for this application.
    config_parser.set_defaults(func=manager.start)

def create_flags():
    parser = argparse.ArgumentParser(prog="zen", description="A simple and configurable code generation tool with user defined templates.")
    parser.add_argument(
        '-p',
        '--project',
        help="Project name. Used to find the project configuration. Ususally stored in the global configuration.",
        type=str,
        default=None
        )
    parser.add_argument(
        '-L',
        '--local-path',
        help="Path of a local configuration file.",
        type=str,
        default=None
        )
    parser.set_defaults(func=start)
    # Create subparsers for applications.
    sub = parser.add_subparsers(help="Extended applications to run")
    config_flags(sub)
    return parser

if __name__ == '__main__':
    # Create all of the flags.
    parser = create_flags()
    # Parse user input to match flags.
    args = parser.parse_args()
    # Run functions.
    args.func(args)
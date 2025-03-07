import argparse

from dynaconf import Dynaconf

parser = argparse.ArgumentParser(
    prog="pacswitch", description="Set up the system's PAC script"
)
parser.add_argument(
    "-c",
    "--conf",
    metavar="path",
    dest="conf",
    type=str,
    action="store",
    help="Configuration file path",
    default=".",
)

settings = Dynaconf(
    settings_files=[parser.parse_args().conf],
)

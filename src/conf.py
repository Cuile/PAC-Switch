import argparse

from dynaconf import Dynaconf

parser = argparse.ArgumentParser(prog="pacswitch", description="设置系统PAC脚本")
parser.add_argument(
    "-c",
    "--conf",
    metavar="path",
    dest="conf",
    type=str,
    action="store",
    help="配置文件路径",
    default=".",
)

settings = Dynaconf(
    settings_files=[parser.parse_args().conf],
)

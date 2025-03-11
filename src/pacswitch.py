import argparse
import signal
import sys
import time
import winreg


def open_pac_proxy(pac_script: str) -> None:
    with winreg.OpenKey(reg_key, reg_sub_key, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, reg_value_name, 0, winreg.REG_SZ, pac_script)  # type: ignore
        winreg.FlushKey(key)
        print("PAC opens successfully, press Ctrl + C to close PAC.")


def close_pac_proxy() -> None:
    with winreg.OpenKey(reg_key, reg_sub_key, 0, winreg.KEY_SET_VALUE) as key:
        try:
            winreg.DeleteValue(key, reg_value_name)
            winreg.FlushKey(key)
            print("PAC closed successfully.")
        except FileNotFoundError:
            print("PAC settings not found in registry.")


def signal_handler(signum, frame):
    close_pac_proxy()
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="pacswitch", description="Set up the system's PAC script"
    )
    parser.add_argument(
        "-u",
        "--url",
        metavar="url",
        dest="pac_script_url",
        type=str,
        action="store",
        help="URL of the PAC script",
        required=True,
    )

    pac_script_url = parser.parse_args().pac_script_url

    reg_key = winreg.HKEY_CURRENT_USER
    reg_sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings"
    reg_value_name = "AutoConfigURL"

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    open_pac_proxy(pac_script_url)

    while True:
        time.sleep(3600)

import argparse
import os
import signal
import sys
import winreg


def open_pac_proxy(pac_script: str) -> None:
    with winreg.OpenKey(reg_key, reg_sub_key, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, reg_value_name, 0, winreg.REG_SZ, pac_script)  # type: ignore
        winreg.FlushKey(key)
        print("PAC opens successfully, press any key to exit & close PAC.")


def close_pac_proxy() -> None:
    with winreg.OpenKey(reg_key, reg_sub_key, 0, winreg.KEY_SET_VALUE) as key:
        try:
            winreg.DeleteValue(key, reg_value_name)
            winreg.FlushKey(key)
            print("PAC closed successfully.")
        except FileNotFoundError:
            print("PAC settings not found in registry.")


def signal_handler(signum, frame):
    sys.exit()


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

    try:
        signal.signal(signal.SIGTERM, signal_handler)
        open_pac_proxy(pac_script_url)
        os.system("pause")
    except SystemExit:
        # term信号触发的退出不做处理
        pass
    finally:
        close_pac_proxy()

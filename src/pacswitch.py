import argparse
import os
import signal
import sys
import time
import winreg


def switch_pac_proxy(pac_script: str) -> None:
    with winreg.OpenKey(reg_key, reg_sub_key, 0, winreg.KEY_SET_VALUE) as key:
        try:
            winreg.DeleteValue(key, reg_value_name)
            winreg.FlushKey(key)
            print("PAC closed successfully.")
        except FileNotFoundError:
            winreg.SetValueEx(key, reg_value_name, 0, winreg.REG_SZ, pac_script)  # type: ignore
            winreg.FlushKey(key)
            print(
                "\nPAC opens successfully. press Ctrl + C or any key to close PAC and exit."
            )


def signal_handler(signum, frame):
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="pacswitch", description="The switch to set the system PAC script."
    )
    parser.add_argument(
        "-u",
        # "--url",
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

    try:
        switch_pac_proxy(pac_script_url)
        time.sleep(1)
        # 由于 supervisor-win 在关闭子进程时，并不会发送 SIGTERM 信号，而是直接调用 Win32 API 的 TerminateProcess() 函数，强制退出进程。
        # 所以只能使用 os.system("pause") 命令将整个进程阻塞，保证程序退出时可以执行 switch_pac_proxy() 函数。
        os.system("pause")
    finally:
        switch_pac_proxy(pac_script_url)

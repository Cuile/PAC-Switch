import os
import signal
import sys
import winreg

from conf import settings as set

reg_key = winreg.HKEY_CURRENT_USER
reg_sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings"
reg_value_name = "AutoConfigURL"
pac_script = set.pac_script


def open_pac_proxy() -> None:
    with winreg.OpenKey(reg_key, reg_sub_key, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, reg_value_name, 0, winreg.REG_SZ, pac_script)
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
    try:
        signal.signal(signal.SIGTERM, signal_handler)
        open_pac_proxy()
        os.system("pause")
    except SystemExit:
        # close_pac_proxy()
        pass
    finally:
        close_pac_proxy()

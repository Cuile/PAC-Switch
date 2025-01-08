import os
import signal
import sys
import winreg

reg_key = winreg.HKEY_CURRENT_USER
reg_sub_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings"
reg_value_name = "AutoConfigURL"
pac_script = "http://localhost:8000/gfwlist.pac"


def open_pac_proxy() -> None:
    with winreg.OpenKey(reg_key, reg_sub_key, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, reg_value_name, 0, winreg.REG_SZ, pac_script)
        winreg.FlushKey(key)
        print("PAC打开成功，按任何键退出 & 关闭PAC。")


def close_pac_proxy() -> None:
    with winreg.OpenKey(reg_key, reg_sub_key, 0, winreg.KEY_SET_VALUE) as key:
        try:
            winreg.DeleteValue(key, reg_value_name)
            winreg.FlushKey(key)
            print("PAC关闭成功。")
        except FileNotFoundError:
            # 如果注册表值已经被删除，则什么也不做
            pass


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

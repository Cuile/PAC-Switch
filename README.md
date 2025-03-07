# PAC Switch
 windows PAC 设置开关

## Build
```powershell
# PyInstaller
> pyi-makespec -F -p . -i .\resources\icon.ico .\src\pacswitch.py
> pyinstaller --clean .\pacswitch.spec

# Nuitka
> python -m nuitka --mingw64 --standalone --onefile --lto=auto `
    --windows-icon-from-ico=.\resources\icon.ico `
    --output-dir=.\nuitka_build --report=.\nuitka_build\build.xml `
    --remove-output --run `
    .\src\pacswitch.py
```

## Use
```powershell
> pacswitch.exe -h
# or
> pacswitch.exe -c .\conf\pac.toml
```

# PAC Switch
 windows PAC 设置开关

## Build
```powershell
> pyi-makespec -F -p . -i .\resources\icon.ico .\src\pacswitch.py
> pyinstaller --clean .\pacswitch.spec
```

## Use
```powershell
> pacswitch.exe -c .\conf\pac.toml
```
echo %1
reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d  %1 /f
%SystemRoot%\System32\RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters

@echo off

"C:\Program Files (x86)\WinSCP\WinSCP.com" ^
  /log="C:\LOGPATH\WinSCP.log" /ini=nul ^
  /command ^
    "open scp://USERNAME:PASSWORD@REMOTESERVER/ -hostkey=""ssh-rsa HOSTKEY""" ^
    "synchronize remote C:\LOCALPATH\ozone /REMOTEPATH/ozone" ^
    "exit"

set WINSCP_RESULT=%ERRORLEVEL%
if %WINSCP_RESULT% equ 0 (
  echo Success
) else (
  echo Error
)

exit /b %WINSCP_RESULT%

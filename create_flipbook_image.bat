@echo off
:: " D&Dしたフォルダに含まれている連番画像からFlipbook画像を作成 "

:: Check argument
if "%1" == "" (
  echo [Warning] フォルダを指定してください
  pause
  exit /b 0
)
if not exist "%1\" (
  echo [Warning] 不正なフォルダパスです
  pause
  exit /b 0
)

:: Python Path
set python_path=".\venv\Scripts\python.exe"

:: Setup Python virtual environment
if not exist venv\  (
    python -m venv venv
    %python_path% -m pip install pillow
)

:: Running Python script
echo python create_flipbook_image.py -i "%1"
%python_path% create_flipbook_image.py -i "%1"

pause
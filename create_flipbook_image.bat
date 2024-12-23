@echo off
:: " D&D�����t�H���_�Ɋ܂܂�Ă���A�ԉ摜����Flipbook�摜���쐬 "

:: Check argument
if "%1" == "" (
  echo [Warning] �t�H���_���w�肵�Ă�������
  pause
  exit /b 0
)
if not exist "%1\" (
  echo [Warning] �s���ȃt�H���_�p�X�ł�
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
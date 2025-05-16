@echo off
echo Installing dsctok package...

python.exe -m pip install --upgrade pip

if exist requirements.txt (
    pip install -r requirements.txt
)

pip install -e .

echo Installation done.

pause>nul

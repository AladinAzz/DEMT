@echo 
REM Automatically find the local IPv4 address (non-loopback)
FOR /F "tokens=2 delims=:" %%A IN ('ipconfig ^| findstr /C:"IPv4 Address"') DO (
    FOR /F "tokens=* delims= " %%B IN ("%%A") DO SET IP=%%B
)

set PORT=8000
echo Starting FastAPI server on %IP%:%PORT%

REM Launch the server
python -m uvicorn main:app --host %IP% --port %PORT% --reload

pause

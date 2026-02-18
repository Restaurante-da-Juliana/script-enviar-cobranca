@echo off
echo Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Erro ao instalar dependencias. Verifique sua conexao ou permissões.
    pause
    exit /b %errorlevel%
)

echo.
echo Iniciando build do aplicativo...
python build_app.py
if %errorlevel% neq 0 (
    echo Erro durante o build.
    pause
    exit /b %errorlevel%
)

echo.
echo Processo concluido com sucesso!
pause

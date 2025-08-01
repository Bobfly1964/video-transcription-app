@echo off
echo ========================================
echo Настройка Git репозитория
echo ========================================

echo.
echo 1. Проверка Git...
git --version
if %errorlevel% neq 0 (
    echo ОШИБКА: Git не установлен!
    echo Скачайте Git с https://git-scm.com/
    pause
    exit /b 1
)

echo.
echo 2. Инициализация Git репозитория...
git init

echo.
echo 3. Добавление файлов...
git add .

echo.
echo 4. Создание первого коммита...
git commit -m "Initial commit: Video Transcription App"

echo.
echo ========================================
echo Git репозиторий успешно настроен!
echo ========================================
echo.
echo Следующие шаги:
echo 1. Создайте репозиторий на GitHub.com
echo 2. Скопируйте URL репозитория
echo 3. Выполните команды:
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo Подробная инструкция в файле GITHUB_SETUP.md
echo.
pause 
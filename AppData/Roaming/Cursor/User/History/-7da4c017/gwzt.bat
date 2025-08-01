@echo off
echo ========================================
echo Исправление Git репозитория
echo ========================================

echo.
echo Текущая папка:
cd
echo.

echo 1. Инициализация Git репозитория...
git init

echo.
echo 2. Добавление файлов проекта...
git add backend/
git add frontend/
git add infrastructure/
git add docker-compose.yml
git add README.md
git add .gitignore
git add GITHUB_SETUP.md
git add QUICK_START.md
git add *.bat
git add *.ps1

echo.
echo 3. Создание первого коммита...
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
pause 
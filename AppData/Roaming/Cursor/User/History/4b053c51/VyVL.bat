@echo off
echo Инициализация Git репозитория...
git init

echo Добавление файлов в Git...
git add .

echo Создание первого коммита...
git commit -m "Initial commit: Video Transcription App"

echo.
echo Git репозиторий настроен!
echo.
echo Теперь выполните следующие шаги:
echo 1. Создайте новый репозиторий на GitHub.com
echo 2. Скопируйте URL репозитория
echo 3. Выполните команды:
echo    git remote add origin YOUR_REPOSITORY_URL
echo    git branch -M main
echo    git push -u origin main
echo.
pause 
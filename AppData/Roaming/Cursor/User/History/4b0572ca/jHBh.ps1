Write-Host "Инициализация Git репозитория..." -ForegroundColor Green
& git init

Write-Host "Добавление файлов в Git..." -ForegroundColor Green
& git add .

Write-Host "Создание первого коммита..." -ForegroundColor Green
& git commit -m "Initial commit: Video Transcription App"

Write-Host ""
Write-Host "Git репозиторий настроен!" -ForegroundColor Green
Write-Host ""
Write-Host "Теперь выполните следующие шаги:" -ForegroundColor Yellow
Write-Host "1. Создайте новый репозиторий на GitHub.com" -ForegroundColor White
Write-Host "2. Скопируйте URL репозитория" -ForegroundColor White
Write-Host "3. Выполните команды:" -ForegroundColor White
Write-Host "   git remote add origin YOUR_REPOSITORY_URL" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Read-Host "Нажмите Enter для продолжения" 
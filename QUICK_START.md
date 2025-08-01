# Быстрый старт - Загрузка на GitHub

## Проблема с PowerShell
В вашей системе PowerShell есть проблема с кодировкой. Используйте обычную командную строку (cmd).

## Пошаговая инструкция:

### 1. Откройте командную строку
- Нажмите `Win + R`
- Введите `cmd`
- Нажмите Enter
- Перейдите в папку проекта: `cd C:\Users\user\video-transcription-app`

### 2. Выполните команды Git
```cmd
git init
git add .
git commit -m "Initial commit: Video Transcription App"
```

### 3. Создайте репозиторий на GitHub
1. Перейдите на [GitHub.com](https://github.com)
2. Нажмите "+" → "New repository"
3. Название: `video-transcription-app`
4. **НЕ** ставьте галочки на README, .gitignore, license
5. Нажмите "Create repository"

### 4. Свяжите с GitHub
Скопируйте URL репозитория и выполните:
```cmd
git remote add origin https://github.com/YOUR_USERNAME/video-transcription-app.git
git branch -M main
git push -u origin main
```

## Альтернативный способ - через GitHub Desktop

1. Скачайте [GitHub Desktop](https://desktop.github.com/)
2. Установите и войдите в аккаунт
3. File → Add local repository
4. Выберите папку `C:\Users\user\video-transcription-app`
5. Publish repository

## Подробная инструкция
См. файл `GITHUB_SETUP.md` для детального описания. 
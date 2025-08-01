# Инструкция по загрузке проекта на GitHub

## Шаг 1: Настройка Git репозитория

Откройте командную строку (cmd) или PowerShell в папке проекта и выполните следующие команды:

```bash
# Инициализация Git репозитория
git init

# Добавление всех файлов
git add .

# Создание первого коммита
git commit -m "Initial commit: Video Transcription App"
```

## Шаг 2: Создание репозитория на GitHub

1. Перейдите на [GitHub.com](https://github.com)
2. Войдите в свой аккаунт
3. Нажмите кнопку "+" в правом верхнем углу
4. Выберите "New repository"
5. Заполните форму:
   - **Repository name**: `video-transcription-app` (или любое другое имя)
   - **Description**: `Full-stack video transcription and note-taking application`
   - Выберите **Public** или **Private**
   - **НЕ** ставьте галочки на "Add a README file", "Add .gitignore", "Choose a license"
6. Нажмите "Create repository"

## Шаг 3: Связывание локального репозитория с GitHub

После создания репозитория GitHub покажет инструкции. Скопируйте URL вашего репозитория (он будет выглядеть как https://github.com/your-username/video-transcription-app.git``)

Выполните следующие команды:

```bash
# Добавление удаленного репозитория
git remote add origin https://github.com/your-username/video-transcription-app.git

# Переименование основной ветки в main
git branch -M main

# Отправка кода на GitHub
git push -u origin main
```

## Шаг 4: Проверка

1. Перейдите на страницу вашего репозитория на GitHub
2. Убедитесь, что все файлы загружены
3. Проверьте, что README.md отображается корректно

## Дополнительные команды

### Для последующих обновлений:
```bash
# Добавление изменений
git add .

# Создание коммита
git commit -m "Описание изменений"

# Отправка на GitHub
git push
```

### Для клонирования репозитория на другом компьютере:
```bash
git clone https://github.com/your-username/video-transcription-app.git
cd video-transcription-app
```

## Настройка GitHub Actions

После загрузки проекта на GitHub:

1. Перейдите в раздел "Actions" вашего репозитория
2. GitHub автоматически обнаружит файл `.github/workflows/ci-cd.yml`
3. Настройте секреты в Settings > Secrets and variables > Actions:
   - `DOCKER_USERNAME` - ваше имя пользователя Docker Hub
   - `DOCKER_PASSWORD` - ваш пароль Docker Hub
   - `KUBECONFIG` - конфигурация Kubernetes (если используете)

## Проблемы и решения

### Если Git не установлен:
1. Скачайте Git с [git-scm.com](https://git-scm.com/)
2. Установите с настройками по умолчанию
3. Перезапустите командную строку

### Если возникает ошибка аутентификации:
1. Настройте SSH ключи или используйте Personal Access Token
2. Для токена: Settings > Developer settings > Personal access tokens > Generate new token
3. Используйте токен вместо пароля при push

### Если файлы не отображаются на GitHub:
1. Проверьте, что файл `.gitignore` не исключает нужные файлы
2. Убедитесь, что выполнили `git add .` и `git commit`
3. Проверьте статус: `git status` 
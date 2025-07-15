# Django Men Project

Учебный Django-проект для хранения информации о людях, их категориях, тегах и связях.  
Проект построен на Django 5+, включает фикстуры с данными и готов к локальному запуску.

##  Стек технологий

-  Django 5+
-  HTML / CSS
-  Python 3.11+
-  SQLite + JSON fixtures
-  venv / requirements.txt

---

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/django-men-project.git
cd django-men-project
```
2. Создайте виртуальное окружение:
```bash
python -m venv djvenv
```
3. Активируйте окружение:
```bash
# Windows (PowerShell)
.\djvenv\Scripts\Activate.ps1

# macOS / Linux
source djvenv/bin/activate
```
4. Установите зависимости:
```bash
pip install -r requirements.txt
```
5. Примените миграции:
```bash
python manage.py migrate
```
6. Загрузите данные из фикстур:
```bash
python manage.py loaddata fixtures/data.json
```
7.Зпустите сервер
```bash
python manage.py runserver
```

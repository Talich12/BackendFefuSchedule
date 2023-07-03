# BackendFefuSchedule
### Вход в вертуальное окружение
```bash
source venv/bin/activate
```
### Подключение всех библиотек
```bash
pip install flask flask_sqlalchemy flask_cors flask_jwt_extended flask_migrate flask_marshmallow marshmallow_sqlalchemy Werkzeug
```
### Инициализация базы данных
```bash
flask db init
```
```bash
flask db migrate -m "init_tables"
```
```bash
flask db upgrade
```
### Запуск
```bash
python3 run.py
```

Foodgram: «Продуктовый помощник»

workflows workflows

«Продуктовый помощник» - это сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Возможности:

Регистрация пользователей
Аутентификация пользователей
Получение и создание рецептов
Добавление рецептов в избранное
Генерация списка покупок для выбранных рецептов
Возможно наделение пользователей правами модерирования и администрирования
Удобная панель администрирования, на русском (требует создание пользователя с правами администратора, средствами движка Django)
Требования (описано в requirements.txt):

Django 4.1.7
djangorestframework 3.14.0
djoser 2.1.0
django-filter 22.1
PyYAML 6.0
coreapi 2.3.3
gunicorn 20.1.0
psycopg2-binary 2.9.6
Pillow 9.4.0
и их зависимости
Установка на тестовом стенде:

Клонировать репозиторий на машину, с которой будет будет запускаться сервис (либо по SSH-ссылке, либо скопировать и распаковать zip-архив). Для работы требуется самостоятельно создать и заполнить файл .env

git clone https://github.com/anzorkhamukov/foodgram-project-react.git
На машине должны быть установлены Docker и Docker-compose актуальной версии

Нужно перейти в папку foodgram-project-react/infra

cd foodgram-project-react/infra
Cобрать контейнер

docker compose up -d --build
Тестовый сервер должен запуститься, и быть доступен по http://127.0.0.1/ Остановка сервера выполняется в Docker.

Для теста панели администратора нужно создать суперпользователя:

docker compose exec web python manage.py createsuperuser
Панель администратора будет доступна по http://127.0.0.1/admin/

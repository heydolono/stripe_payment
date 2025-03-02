# stripe_payment

Этот проект представляет собой бэкенд на Django с интеграцией Stripe API, позволяющий:

 - Создавать товары с ценой и описанием.

 - Оплачивать отдельные товары через Stripe Checkout.

 - Создавать заказы из нескольких товаров и оплачивать их одним платежом.

 - Использовать скидки и налоги при оплате заказа.

## Установка

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:heydolono/stripe_payment.git
```
```
cd stripe_payment/infra
```

### Настройка переменных окружения:

Переименуйте .env.example в .env и заполните переменные

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=SECRET_KEY_DJANGO (Заполнить)
STRIPE_TEST_SECRET_KEY=sk_test_****** (Заполнить)
STRIPE_TEST_PUBLISHABLE_KEY=pk_test_******  (Заполнить)
```

### Запустить Docker Compose и выполнить команды:
```
docker compose up -d
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py collectstatic --noinput
```

## Использование

Админка доступна по

```
127.0.0.1/admin
```

1. Создание товара (Item)

Можно создать через Django Admin, доступен по:

```
127.0.0.1/item/{id}
```

2. Оплата товара

Перейдите по URL /item/{id} и нажмите кнопку "Купить товар".

3. Создание заказа (Order)

Заказы можно создавать через Django Admin, добавляя в них несколько товаров, доступен по:

```
127.0.0.1/order/{id}
```

4. Оплата заказа

Перейдите по URL /order/{id} и нажмите "Оплатить заказ".

## Разработчик
- [Максим Колесников](https://github.com/heydolono)
- [Резюме](https://career.habr.com/heydolono)
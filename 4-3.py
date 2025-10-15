import time
import requests

class Test:
    # Базовая ссылка на api
    url = "https://api.chucknorris.io/jokes"

    def get_categories(self, expected_status_code):
        # Формируем путь к ручке с категориями
        path_url = f"{self.url}/categories"

        # Запрашиваем массив категорий
        response = requests.get(path_url)

        # Проверим, что статус-код запроса соответствует аргументу
        assert(response.status_code == expected_status_code)

        # Смотрим содержимое
        categories = response.json()
        print(categories)

        # Возвращаем массив
        return categories

    def get_joke_by_category(self, category, expected_status_code):
        # Ручка для получения шутки по категории
        path_url = f"{self.url}/random?category={category}"
        print(path_url)

        # Делаем запрос
        response = requests.get(path_url)
        print(response.json())

        # Проверяем статус код на корректность
        assert response.status_code == expected_status_code
        print('Запрос выполнен успешно')

        # Получаем категорию шутки из массива категорий
        joke_category = response.json()['categories'][0]

        # Проверяем, что запрос отработал корректно и категория соответствует запрашиваемой
        assert joke_category == category
        print('Категория корректна')

        # Получаем содержимое шутки
        joke_value = response.json()["value"]
        print(f'Шутка: {joke_value}\nКатегория: {category}')

    def get_joke_from_every_category(self):
        # Получаем актуальные категории из api
        categories = self.get_categories(200)

        # По каждой категории делаем запрос на шутку
        for category in categories:
            self.get_joke_by_category(category, 200)
            # Добавляем кулдаун между запросами, чтобы не вызвать ошибок
            time.sleep(2)


# Создаем объект класса с тестами
test = Test()

# Запускаем необходимый тест из класса
test.get_joke_from_every_category()
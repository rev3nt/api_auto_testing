import requests

class Test:
    # Базовая ссылка на api
    url = "https://api.chucknorris.io/jokes"

    def varify_category_and_get_joke(self, category, expected_status_code):
        # Формируем путь к ручке с категориями
        path_url = f"{self.url}/categories"

        # Запрашиваем массив категорий
        response = requests.get(path_url)

        # Проверим, что статус-код запроса соответствует аргументу
        assert(response.status_code == expected_status_code)

        # Смотрим содержимое
        categories = response.json()
        print(categories)

        # Проверяем, есть ли категория в api
        assert category in categories
        print("Категория найдена в списке!")

        # Вызываем функцию на получение шутки по категории
        self.get_joke_by_category(category, 200)

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


# Создаем объект класса с тестами
test = Test()

# Запускаем необходимый тест из класса
user_input = input("Введите категорию, по которой хотите получить шутку: ")

# Получаем шутку по категории
test.varify_category_and_get_joke(user_input, 200)
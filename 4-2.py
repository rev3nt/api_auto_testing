import requests


class Test:
    url = "https://api.chucknorris.io"

    def test_get_joke_by_category(self, category_name):
        # Собираем URL, добавляя фильтр по введенной категории
        random_joke_by_category_path = f'{self.url}/jokes/random?category={category_name}'

        # Делаем запрос по сформированной ссылке
        response = requests.get(random_joke_by_category_path)
        print("Запрос отправлен")

        # Проверяем, что запрос отработал с корректным статус кодом
        assert response.status_code == 200
        print("Запрос отработал корректно")

        # Получаем категорию из json
        joke_category = response.json()['categories'][0]

        # Сравниваем категорию на соответствие запрашиваемой в аргументах метода
        assert joke_category == category_name
        print("Категория корректна")

        # Извлекаем шутку из json
        joke_text = response.json()['value']

        # Проверяем, есть ли слово "Chuck" в шутке
        if "chuck" in joke_text.lower():
            print('Слово "chuck" присутствует в тексте шутки')
        else:
            print('Слово "chuck" отсутствует в тексте шутки')

        print(joke_text)


# Создаем экземпляр тестового класса
test = Test()

# Вызываем метод с тестом
test.test_get_joke_by_category("sport")
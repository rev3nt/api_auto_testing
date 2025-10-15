import requests

# URL ручки, к которой будем обращаться
url = "https://api.chucknorris.io/jokes/random"
# Вывод URL
print(url)

# Делаем запрос к api с помощью метода get
response = requests.get(url)
# Выводим статус кода ответа
print(response.status_code)

# Проверяем статус код на соответствие ожидаемому результату
assert response.status_code == 200
print("Запрос отработал корректно")

# Выводим текст ответа в формате JSON
print(response.text)
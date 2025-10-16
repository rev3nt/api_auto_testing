import requests

from test_put import PutTest


class Test:
    # Базовый url
    url = "https://rahulshettyacademy.com"

    # Стандартный json, который будет использоваться в POST запросе
    payload = {"location": {
        "lat": -38.383494,
        "lng": 33.427362
    }, "accuracy": 50,
        "name": "Frontline house",
        "phone_number":
            "(+91) 983 893 3937",
        "address": "29, side layout, cohen 09",
        "types": ["shoe park", "shop"],
        "website": "http://google.com",
        "language": "French-IN"}

    # Функция для создания ресурса
    def test_post_location(self):
        # Формируем url для создания нового места на карте
        path_url = f'{self.url}/maps/api/place/add/json/key=qaclick123'
        print(path_url)

        # Делаем запрос
        post_response = requests.post(path_url, json=self.payload)

        # Проверяем статус-код на корректность
        assert post_response.status_code == 200
        print("POST запрос успешно выполнен")

        # Преобразуем ответ в json
        post_response_json = post_response.json()
        # Извлекаем статус
        post_response_status = post_response_json['status']

        # Проверяем тело ответа сервера на соответствие статус коду
        assert post_response_status == 'OK'
        print('Локация успешно размещена в API')

        print(post_response_json)

        # Возвращаем id созданного места
        return post_response_json['place_id']

    # Функция для проверки корректности созданного ресурса по id
    def test_get_location(self, place_id):
        # Формируем url для GET запроса
        path_url = f'{self.url}/maps/api/place/get/json?key=qaclick123&place_id={place_id}'
        print(path_url)

        # Делаем запрос
        get_response = requests.get(path_url)

        # Проверяем статус-код на корректность
        assert get_response.status_code == 200
        print("GET запрос успешно выполнен")

        # Преобразуем в тело ответа в json
        get_response_json = get_response.json()
        print(get_response_json)

        # Извлекаем из json поля для проверки на соответствие изначальному пейлоаду
        lat = get_response_json['location']['latitude']
        lng = get_response_json['location']['longitude']
        name = get_response_json['name']

        # Проверяем поля, найдя нужные ключи и приведя все данные к одному типу
        assert lat == str(self.payload['location']['lat'])
        assert lng == str(self.payload['location']['lng'])
        assert name == str(self.payload['name'])
        print("Локация корректна сохранена")

        # Возвращаем json, полученный из ответа
        return get_response_json

    def test_put_request(self):
        # Формируем ссылку для PUT запроса
        path_url = f"{self.url}/maps/api/place/update/json?key=qaclick123"

        # Создаем локацию
        place_id = self.test_post_location()

        # Помещаем json, созданной локации
        unedited_location = self.test_get_location(place_id)

        # Создаем экземпляр тестового класса из файла для выполнения PUT запроса
        put_tester = PutTest(path_url, place_id)

        # Вызываем функцию выполнения запроса
        put_tester.put_request()

        # Получаем новый json с измененными данными
        edited_location = self.test_get_location(place_id)

        # Сравниваем отредактированные поля
        assert unedited_location['address'] != edited_location['address']
        print("Адрес был успешно изменен")

        # Сравниваем неотредактированные поля
        assert unedited_location['location']['latitude'] == edited_location['location']['latitude']
        print("Данные, не переданные в PUT запросы остались неизменными")

        print("Тест успешно завершен")

# Создаем экземпляры класса
test = Test()

# Выполняем метод тестирования PUT запроса
test.test_put_request()
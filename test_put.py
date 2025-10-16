import requests

from BigTestClass import Test


class PutTest:
    def __init__(self,url, place_id = ''):
        self.url = url
        self.place_id = place_id

    def put_request(self):
        put_payload = {"place_id": self.place_id,
                       "address": "100 Lenina street, RU",
                       "key": "qaclick123"}

        put_response = requests.put(url=self.url, json=put_payload)

        response_status_code = put_response.status_code
        print("PUT успешно выполнен")

        assert response_status_code == 200
        print("Статус код ответа корректен")

        response_json = put_response.json()
        response_message = response_json["msg"]

        successful_message = "Address successfully updated"

        assert response_message == successful_message
        print("Запрос выполнен успешно")

    def test_put(self):
        # Создаем экземпляр класса, в который передаем url для запроса и id локации для редактирования

        # Создаем экземпляр тестового класса
        api = Test()

        # Создаем локацию
        self.place_id = api.test_post_location()

        # Помещаем json, созданной локации
        unedited_location = api.test_get_location(self.place_id)

        # Изменяем локацию
        self.put_request()

        # Получаем новый json с измененными данными
        edited_location = api.test_get_location(self.place_id)

        # Сравниваем отредактированные поля
        assert unedited_location['address'] != edited_location['address']
        print("Адрес был успешно изменен")

        # Сравниваем неотредактированные поля
        assert unedited_location['location']['latitude'] == edited_location['location']['latitude']
        print("Данные, не переданные в PUT запросы остались неизменными")

        print("Тест успешно завершен")
import requests


class PutTest:
    def __init__(self,url, place_id):
        self.url = url
        self.place_id = place_id

    def put_request(self):
        # Формируем тело PUT запроса
        put_payload = {"place_id": self.place_id,
                       "address": "100 Lenina street, RU",
                       "key": "qaclick123"}

        # Делаем запрос к API
        put_response = requests.put(url=self.url, json=put_payload)

        # Получаем статус код запроса
        response_status_code = put_response.status_code
        print("PUT успешно выполнен")

        # Выполняем проверку соответствия статус кода к ожидаемому результату
        assert response_status_code == 200
        print("Статус код ответа корректен")

        # Преобразуем ответ в json
        response_json = put_response.json()

        # Извлекаем сообщение из json
        response_message = response_json["msg"]

        # Записываем ожидаемый результат полученного сообщения
        successful_message = "Address successfully updated"

        # Выполняем проверку, соответствует ли сообщение в json ожидаемому результату
        assert response_message == successful_message
        print("Запрос выполнен успешно")
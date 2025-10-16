import requests


class DeleteTest:
    def __init__(self, url):
        self.url = url

    def delete_request(self, place_id):
        payload = {"place_id": place_id}

        response = requests.delete(self.url, json=payload)
        print("DELETE запрос был успешно отправлен")

        assert response.status_code == 200
        print("Статус код запроса корректен")

        response_json = response.json()

        assert response_json["status"] == "OK"
        print("Запрос успешно выполнен")
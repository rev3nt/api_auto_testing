import requests

from test_put import PutTest
from test_delete import DeleteTest


class Test:
    # Базовый url
    url = "https://rahulshettyacademy.com"
    # Путь до файла с сохраненными id мест
    file_path = 'C:\\Users\\user\\PycharmProjects\\api_autotesting\\place_id'

    clean_file_path = 'C:\\Users\\user\\PycharmProjects\\api_autotesting\\clean_place_id'

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

    # Конструктор будет чистить файл при создании тестового экземпляра
    def __init__(self):
        self.clear_file(self.file_path)
        self.clear_file(self.clean_file_path)

    def clear_file(self, path):
        with open(path, "w") as file:
            file.write("")

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
        if get_response.status_code != 200:
            print("Запрашиваемый ресурс не найден (404)")

            return get_response.json()

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

    # Функция сохраняющая в файл id, созданных ресурсов, создает и сохраняет count количество id
    def save_place_id_to_file(self, file_path, count=0, place_id = ''):
        # Если в функцию передается id, то он сохраняется в файл
        if place_id:
            with open(file_path, "a") as file:
                file.write(place_id + "\n")

        else:
            # Если в функцию не передается id, то в файле генерируется count количество локаций
            with open(file_path, "a") as file:
                for i in range(count):
                    file.write(self.test_post_location() + "\n")

    # Функция для чтения содержимого файла с id
    def read_place_id_from_file(self):
        # Массив с сохраненными id
        place_ids = []

        # Открываем файл на чтение и записываем каждую строку в массив
        with open(self.file_path, "r") as file:
            for word in file:
                place_ids.append(word.strip())

        # Возвращаем массив id
        return place_ids

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

    def delete_if_id_not_exists(self):
        # Выгружаем id локаций в список
        ids = self.read_place_id_from_file()

        # Проходимся по id
        for place_id in ids:
            # Делаем GET запросы по id и сохраняем json
            response = self.test_get_location(place_id)

            # Смотрим, есть ли в json поле msg, если да, то это говорит о том, что ресурса нет в API
            if 'msg' in response:
                print(f"Локация с id {place_id} отсутствует в api")

            else:
                # Если id есть в API, то мы сохраняем его в специальный файл
                self.save_place_id_to_file(self.clean_file_path, place_id=place_id)
                print(f"Локация с id {place_id} числится в api")

    def test_delete_request(self):
        # Чистим файл, если в нем остались данные от других проверок
        self.clear_file(self.file_path)

        # Создаем 5 id в файле
        self.save_place_id_to_file(self.file_path, count=5)

        # Считываем информацию из файла в список
        ids = self.read_place_id_from_file()

        # Собираю url для удаления ресурса с помощью метода DELETE
        path_url = f"{self.url}/maps/api/place/delete/json?key=qaclick123"

        # Создаю экземпляр класса для теста удаления
        delete_tester = DeleteTest(path_url)

        # Вызываю метод удаления ресурса по 2 id из файла
        delete_tester.delete_request(ids[1])

        # Вызываю метод удаления ресурса по 4 id из файла
        delete_tester.delete_request(ids[3])

        # Запускаю проверку id в файле на наличие в API
        self.delete_if_id_not_exists()


# Создаем экземпляры класса
test = Test()

# Выполняем метод тестирования DELETE запроса
test.test_delete_request()
print("Тест завершен успешно")
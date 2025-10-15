import requests


class Test:
    # Базовый url
    url = "https://rahulshettyacademy.com"

    # Путь до файла с сохраненными id мест
    file_path = 'C:\\Users\\user\\PycharmProjects\\api_autotesting\\place_id'

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
        with open(self.file_path, "w") as file:
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
        assert get_response.status_code == 200
        print("Запрос успешно выполнен")

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

    # Функция сохраняющая в файл id, созданных ресурсов, создает и сохраняет count количество id
    def save_place_id_to_file(self, count):
        # Открывает файл и записываем созданные с помощью метода id мест
        with open(self.file_path, "a") as file:
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

# Создаем экземпляр тестового класса
api = Test()

# Создаем и сохраняем необходимое количество мест в файл
api.save_place_id_to_file(count=5)

# Читаем и записываем все созданные id в список
places = api.read_place_id_from_file()

# Проводим тест по каждому id на соответствие пейлоаду
for place in places:
    api.test_get_location(place)

print("Тест успешно завершен")
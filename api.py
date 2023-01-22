import json
import requests
import uuid
import os.path
from settings import VALID_EMAIL, VALID_PASSWORD, ID_ATOS, ID_ARAMIS, ID


class Pets:
    """ API библиотека к сайту http://34.141.58.52:8080/#/ """

    def __init__(self):
        self.base_url = 'http://34.141.58.52:8000/'

    def get_registered_and_delete(self) -> json:
        """ Регистрация и удаление пользователя в Swagger сайта через post/register -> delete/users/{id} """
        e = uuid.uuid4().hex
        data = {"email": f'olga@{e}.ru',
                "password": 'olga', "confirm_password": 'olga'}
        res = requests.post(self.base_url + 'register', data=json.dumps(data))
        my_id = res.json().get('id')
        my_token = res.json()['token']
        headers = {'Authorization': f'Bearer {my_token}'}
        params = {'id': my_id}
        res = requests.delete(self.base_url + f'users/{my_id}', headers=headers, params=params)
        status = res.status_code
        return status

    def get_token(self) -> json:
        """ Запрос к Swagger сайта для получения уникального токена пользователя по указанным email и password,
         прохождение авторизации через post/login """
        data = {"email": VALID_EMAIL,
                "password": VALID_PASSWORD}
        res = requests.post(self.base_url + 'login', data=json.dumps(data))
        my_token = res.json()['token']
        my_email = res.json()['email']
        my_id = res.json()['id']
        status = res.status_code
        return my_token, my_email, my_id, status

    def get_list_users(self):
        """ Получение списка пользователей в Swagger сайта авторизованным пользователем через get/users
        (по факту получение нашего id - баг в Swagger)"""
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.get(self.base_url + 'users', headers=headers)
        status = res.status_code
        my_id = res.text
        return status, my_id

    def get_pet(self):
        """ Создание нового питомца в Swagger сайта авторизованным пользователем через post/pet
        (количество созданных одинаковых питомцев может задваиваться - баг)"""
        my_token = Pets().get_token()[0]
        my_id = Pets().get_token()[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"id": my_id,
                "name": 'R', "type": 'cat', "age": 2, "gender": 'Female', "owner_id": my_id}
        res = requests.post(self.base_url + 'pet', data=json.dumps(data), headers=headers)
        pet_id = res.json()['id']
        status = res.status_code
        return pet_id, status

    def get_pet_photo(self):
        """ Добавление фото новому питомцу в Swagger сайта авторизованным пользователем через post/pet/{id}/image
        (создаются два одинаковых питомца - один с фото и один без - баг) """
        my_token = Pets().get_token()[0]
        pet_id = Pets().get_pet()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        pic_path = os.path.join(os.path.dirname(__file__), 'tests/photo/R.jpg')
        files = {'pic': ('R.jpg', open(pic_path, 'rb'), 'image/jpg')}
        res = requests.post(self.base_url + f'pet/{pet_id}/image', headers=headers, files=files)
        status = res.status_code
        link = res.json()['link']
        return status, link

    def get_pet_like(self):
        """ Проставление лайка своему питомцу в Swagger сайта авторизованным пользователем через put/pet/{id}/like,
        зная id уже имеющегося питомца (ставится только 1 раз - далее ошибка 403 - метка xfail) """
        my_token = Pets().get_token()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"id": ID_ATOS}
        res = requests.put(self.base_url + f'pet/{ID_ATOS}/like', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def get_pet_like_save_pet(self):
        """ Проставление лайка своему питомцу в Swagger сайта авторизованным пользователем через put/pet/{id}/like,
        зная pet_id созданного выше питомца (количество одного и того же питомца с лайком затраивается или
        задваивается - баг) """
        my_token = Pets().get_token()[0]
        pet_id = Pets().get_pet()[0]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"id": pet_id}
        res = requests.put(self.base_url + f'pet/{pet_id}/like', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def add_pet_like(self):
        """ Создание нового питомца в Swagger сайта авторизованным пользователем через post/pet и
        добавление ему лайка через put/pet/{id}/like (создаются два питомца с лайками - баг)"""
        my_token = Pets().get_token()[0]
        my_id = Pets().get_token()[2]
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"id": my_id,
                "name": 'M', "type": 'cat', "age": 2, "gender": 'Female', "owner_id": my_id}
        res = requests.post(self.base_url + 'pet', data=json.dumps(data), headers=headers)
        pet_id_1 = res.json()['id']
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"id": pet_id_1}
        res = requests.put(self.base_url + f'pet/{pet_id_1}/like', data=json.dumps(data), headers=headers)
        status = res.status_code
        return status

    def add_pet_comment(self):
        """ Оставление комментария своему питомцу в Swagger сайта авторизованным пользователем через
        put/pet/{id}/comment, зная id уже имеющегося питомца (создается два одинаковых комментария - баг) """
        my_token = Pets().get_token()[0]
        pet_id_2 = ID_ARAMIS
        headers = {'Authorization': f'Bearer {my_token}'}
        data = {"pet_id": pet_id_2, "date": "2022-12-05T10:52:41.669Z", "message": 'Wow!My pet!', "user_id": ID,
                "user_name": VALID_EMAIL, }
        res = requests.put(self.base_url + f'pet/{pet_id_2}/comment', data=json.dumps(data), headers=headers)
        status = res.status_code
        id_comment = res.json()['id']
        return status, id_comment

    def get_pet_id(self):
        """ Получение характеристик своего питомца в Swagger сайта авторизованным пользователем через
            get/pet/{id}, зная id уже имеющегося питомца
            (команда отрабатывает, но могут создаваться копии питомцев - баг) """
        my_token = Pets().get_token()[0]
        pet_id_2 = ID_ARAMIS
        headers = {'Authorization': f'Bearer {my_token}'}
        res = requests.get(self.base_url + f'pet/{pet_id_2}', headers=headers)
        status = res.status_code
        id_pet = res.json()['pet']['id']
        name_pet = res.json()['pet']['name']
        gender = res.json()['pet']['gender']
        owner_id = res.json()['pet']['owner_id']
        type_pet = res.json()['pet']['type']
        return status, id_pet, name_pet, gender, owner_id, type_pet


Pets().get_registered_and_delete()
Pets().get_token()
Pets().get_list_users()
Pets().get_pet()
Pets().get_pet_photo()
Pets().get_pet_like()
Pets().get_pet_like_save_pet()
Pets().add_pet_like()
Pets().add_pet_comment()
Pets().get_pet_id()

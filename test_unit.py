import json
import re
import unittest
import pickle
import requests

from main import *
from register import User, Grade, return_sqlalchemysession


class TestsFlaskMethods(unittest.TestCase):

    def setUp(self):
        print("Rozpoczęto testowanie")

    def test_czy_podane_poprawne_miato_pojawia_sie_w_otrzymywanym_jsonie_z_API(self):
        self.testowane_miasto = "Krakow"  # Poznań, Kraków
        api_key = "Your API key goes here" #!
        self.weatherjson = json.loads(requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={self.testowane_miasto}&appid={api_key}').content.strip())
        self.assertIsInstance(self.weatherjson["main"], dict, "weather main is not dict")
        self.assertIsInstance(self.weatherjson["name"], str)
        self.assertTrue(self.testowane_miasto == self.weatherjson['name'],
                        f"Otrzymane miasto z API {self.weatherjson['name']} nie jest takie samo jak podane miasto {self.testowane_miasto}")

    def test_unikatowy_username_przechodzi_pozytywnie_rejestracje(self):
        sqlsession = return_sqlalchemysession()
        u_username = "admin"
        u_password = "admin"
        self.assertIsInstance(u_username, str, "Zadeklarowany przykład nazwy usera jest typem string")
        self.assertIsInstance(u_password, str, "Zadeklarowany przykład hasla usera jest typem string")
        user = User(u_username, u_password)
        self.assertIsInstance(user, User, "Testowany przykład uzytkownika jest klasą User")
        sqlsession.add(user)
        sqlsession.commit()
        test_username = "fest"
        test_password = "password"
        self.assertIsInstance(test_username, str, "Testowany przykład nazwy usera jest typem string")
        self.assertIsInstance(test_password, str, "Testowany przykład hasla usera jest typem string")
        test_user = User(test_username, test_password)
        query = sqlsession.query(User).filter(User.username.in_([test_user.username]))
        query = query.first()
        self.assertIsNone(query, f"W bazie użytkowników jest obiekt o takim username {test_user.username}")

    def test_istnieje_baza_ocen(self):
        sqlsession = return_sqlalchemysession()
        test_grade = sqlsession.query(Grade).first()
        self.assertIsInstance(test_grade, Grade, "Baza ocen nie zawiera ani jednej oceny")

    def test_baza_danych_zawiera_wiecej_niz_1000_ocen(self):
        sqlsession = return_sqlalchemysession()
        test_amount_grades = len(sqlsession.query(Grade).all())
        self.assertGreater(test_amount_grades, 1000,
                           f"Baza ocen zawiera mniej niż 1000 ocen, a dokładnie to {test_amount_grades}")

    def test_usuniecie_ostatniej_oceny_zmniejsza_liczbe_ocen_w_bazie(self):
        sqlsession = return_sqlalchemysession()
        test_amount_grades = len(sqlsession.query(Grade).all())
        last_grade = sqlsession.query(Grade).order_by(Grade.id.desc()).first()
        sqlsession.delete(last_grade)
        test_amount_grades_after = len(sqlsession.query(Grade).all())
        self.assertEqual(test_amount_grades_after, test_amount_grades - 1,
                         f"Usunięcie ostatniej oceny nie powiodło się, Liczba ocen przed usunięciem to: {test_amount_grades}, a po usunięciu to: {test_amount_grades_after}")

    def test_czy_plik_z_labelami_zostal_zaladowany_poprawnie(self):
        self.file_path = "labels.pkl"
        self.assertIsInstance(self.file_path, str, "Nazwa pliku nie jest stringiem")
        self.assertRegex(self.file_path, re.compile('.*(.pkl)$'), "Nie rozpoznano rozszerzenia pliku ")
        self.encoder_dict = pickle.load(open(self.file_path, "rb"))
        self.assertIsInstance(self.encoder_dict, dict, "Wczytany plik nie jest słownikiem")

    def test_czy_plik_z_labelami_posiada_odpowiednie_klucze(self):
        self.file_path = "labels.pkl"
        self.encoder_dict = pickle.load(open(self.file_path, "rb"))
        self.assertIn('Vehicle_brand', self.encoder_dict.keys(), "Vehicle_brand plik nie zawiera informacji o modelach samochodow")

    def tearDown(self):
        print("Zakończono testowanie")

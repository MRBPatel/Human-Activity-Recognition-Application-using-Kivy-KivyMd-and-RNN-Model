from kivy.uix.boxlayout import BoxLayout

from utils import DataBase

_db = DataBase("db.db")



class Session:
    _user = None

    @classmethod
    def create(cls, user):
        cls._user = user

    @classmethod
    def get_user(cls):
        return cls._user

    @classmethod
    def clear(cls):
        cls._user = None



class UserLoginPage(BoxLayout):
    def __init__(self, _parent, **kwargs):
        super().__init__(**kwargs)
        self._parent = _parent

    def login(self, username, password):
        users = _db.selection(f"SELECT * FROM user", False)
        for i in users:
            if i['username'] == username and i['password']:
                Session.create(i)
                print(f"{username} is now Logged-in")
                self._parent.load_dashboard_page()
                break

        if Session.get_user() is None:
            print(f"{username} is not registered")

    def call_signup(self):
        self._parent.load_signup()

    # Builder.load_string("""


class UserRegistrationPage(BoxLayout):
    def __init__(self, _parent, **kwargs):
        super().__init__(**kwargs)
        self._parent = _parent

    def register_user(self):
        data = {key: self.ids[key].text for key in ("username", "password", "name",
                                                    "age", "movement_profile", "height", "weight", "job")}
        if _db.insert("user", data):
            print("user registration successfully")
            self.home()

        else:
            print("Registration Failed")

    def home(self):
        self._parent.homepage()
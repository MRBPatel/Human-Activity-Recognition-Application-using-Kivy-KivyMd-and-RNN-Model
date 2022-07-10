from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen

import permission_sensors
from activity_recogniser_model import ActiveSensorData, ActivityRecogniser
from graph import Graph
from buttons_icon_css import RoundedButton
from user_register_login import UserLoginPage, UserRegistrationPage, Session
from motivation_manager import MotivationManagerModel
from db_engine import DataBase, RsaEncryption

RsaEncryption.init()
ActiveSensorData.init()
_dbEngine = DataBase("db.db")
analyser = ActivityRecogniser()

Window.size = (320, 550)

""" Main Dashboard of the app, here calling all the created function in order to
 use in main screen"""


class MainDashboardPage(BoxLayout):

    def __init__(self, _parent, **kwargs):
        super().__init__(**kwargs)
        self._parent = _parent

    @property
    def checking(self):
        return getattr(self, "_checked_in", False)

    @checking.setter
    def checking(self, value):
        setattr(self, "_checked_in", value)

    @property
    def PAUSE(self):
        return getattr(self, "_pause", False)

    @PAUSE.setter
    def PAUSE(self, value):
        setattr(self, "_pause", value)

    def read_motivation_task(self, key):
        try:
            userid = Session.get_user()['user_id']
            tasks = _dbEngine.selection(f"SELECT * FROM motivation WHERE userid='{userid}'", True)
            return tasks[key.lower()]

        except Exception as error:
            print(error)

    def set_message(self, message):
        self.ids.lbl_msg.text = message

    def analyse(self, dt):
        def _analyse(result, dt):
            if result is not None:
                if not self.PAUSE:
                    task = self.read_motivation_task(result)
                    if task is not None:
                        self.set_message(task)
                    else:
                        self.set_message("You are " + result)
                else:
                    self.set_message("notification paused")
            else:
                self.set_message("analyses failed - will try again")

        self.set_message(" Processing >>>>")
        analyser.analyse(ActiveSensorData.data_sequence(90), _analyse)

    def checkin_analyser(self):
        if not self.checking:
            Clock.schedule_interval(self.analyse, 5)
            self.checking = True
            self.set_message(" Now start analysing your activity ")

    def checkout_analyser(self):
        if self.checking:
            Clock.unschedule(self.analyse)
            self.checking = False
            self.set_message(" stopped analysing your activity ")

    def call_login_form(self):
        Session.clear()
        self._parent.homepage()

    def call_motivational_task_model(self):
        popup = MotivationManagerModel(self)
        popup.load_modal()

    def call_graph_model(self):
        Graph().open()

    def call_pause_modal(self):
        self.PAUSE = not self.PAUSE

    def call_settings(self):
        pp = Setting(self)
        pp.show()


class Setting(ModalView):  # creating class to edit user details
    def __init__(self, _parent, **kwargs):
        super().__init__(**kwargs)
        self._parent = _parent

    def _read_records(self):
        """ read & populate records from database table """

        try:
            userid = Session.get_user()['user_id']
            data = _dbEngine.selection(f"SELECT * FROM user WHERE user_id='{userid}'", True)
            return data

        except Exception as error:
            print(error)

    def show(self):
        """ display setting popup """
        data = self._read_records()
        if data is not None:
            for key in ("name", "username", "weight", "height", "age", "job"):
                self.ids[key].text = data[key]
                self.ids.btn_action.text = "update"

            self.open()

    def set_message(self, message):
        t = message
        return t

    def save_records(self, source, name, age, height, weight, job, username):
        userid = Session.get_user()["user_id"]
        if source == "Save":
            data = {"user_id": userid, "name": name, "age": age, "height": height, "weight": weight, "job": job,
                    "username": username}
            if _dbEngine.save("user", data):
                self.set_message("user data saved successfuly")
                self.ids.btn_action.text = "save"
                self._parent.load_dashboard_page()

            else:
                self.set_message("failed to save data - try again")

        else:
            data = {"user_id": userid, "name": name, "age": age, "height": height, "weight": weight, "job": job,
                    "username": username}
            if _dbEngine.update("user", data, f"userid='{userid}'"):
                self.set_message("user data updated successfully")
                self.ids.btn_action.text = "Update"
                self._parent.load_dashboard_page()


            else:
                self.set_message("error updating user data")

    def close_model(self):
        self.dismiss()
        self.ids.btn_action.text = "save"
        self.set_message("")


class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dynamic_area = self.ids.dynamic_box
        self.homepage()

    def homepage(self):
        self.admin_register = True

        self.login_form = UserLoginPage(self)
        self.register_page = UserRegistrationPage(self)

        self.dynamic_area.clear_widgets()
        if self.admin_register:
            self.dynamic_area.add_widget(self.login_form)
        else:
            self.dynamic_area.add_widget(self.register_page)

    def load_signup(self):
        self.dynamic_area.clear_widgets()
        self.dynamic_area.add_widget(self.register_page)

    def load_dashboard_page(self):
        self.dashboard_page = MainDashboardPage(self)
        self.dynamic_area.clear_widgets()
        self.dynamic_area.add_widget(self.dashboard_page)


class MainApp(App):
    def build(self):
        return Main()


if __name__ == "__main__":
    MainApp().run()

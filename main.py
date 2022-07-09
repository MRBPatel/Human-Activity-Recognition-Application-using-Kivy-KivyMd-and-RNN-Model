from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen

import permission_sensors
from activity_recogniser_model import ActiveSensorData, ActivityRecogniser, PauseModel
from graph import Graph
from user_register_login import UserLoginPage, UserRegistrationPage, Session
from motivation_manager import MotivationManagerModel
from buttons_icon_css import RoundedButton
from utils import DataBase, RsaEncryption

RsaEncryption.init()
ActiveSensorData.init()
_dbEngine = DataBase("db.db")
analyser = ActivityRecogniser()

Window.size = (320, 550)


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
            userid = Session.get_user()['id']
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

    def call_motivational_task_modal(self):
        popup = MotivationManagerModel(self)
        popup.load_modal()

    def call_graph_modal(self):
        Graph().open()

    def call_pause_modal(self):
        self.PAUSE = not self.PAUSE

    def call_settings(self):
        return Setting(self).show()



# classes reperesenting systemPermission
class SystemPermission(Screen):

    def allowAccelerometer(self):
        permission_sensors.allowAccelero

    def allowGyrometer(self):
        permission_sensors.allowGyro

    def allowStorage(self):
        permission_sensors.memoryAccess


class Setting(ModalView):
    def __init__(self, main_parent, **kwargs) -> None:
        super(Setting, self).__init__(**kwargs)
        self._main_parent = main_parent

    def _read_records(self):
        """ read & populate records from database table """
        data = _dbEngine.read("user")
        if data is not None:
            for key, val in data.items():
                self.ids[key].text = val
            self.ids.btn_action.text = "Update"

    def show(self):
        """ display setting popup """
        self._read_records()
        self.open()

    def save_records(self, type):
        """ save records into the database
            >>> @param:type -> [Save/Update] flag to decide db operation
        """
        data = {}
        for key in ("username", "age", "weight", "height", "job"):
            data[key] = self.ids[key].text

        if type == "Save":
            _dbEngine.save("user", data)

        else:
            _dbEngine.update("user", data)

        self.close_popup()

    def close_popup(self):
        self.dismiss()


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
        if self.admin_register == True:
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

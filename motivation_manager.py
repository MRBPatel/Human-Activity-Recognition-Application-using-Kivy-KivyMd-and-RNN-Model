from kivy.uix.modalview import ModalView

from user_register_login import Session
from db_engine import DataBase

_db = DataBase("db.db")

"""creating class to use motivational task within this class user can add motivation task or update task"""


class MotivationManagerModel(ModalView):
    def __init__(self, _parent, **kwargs):
        super().__init__(**kwargs)
        self._parent = _parent

    def read_motivation_tasks(self):
        try:
            userid = Session.get_user()['user_id']
            tasks = _db.selection(f"SELECT * FROM motivation WHERE userid='{userid}'", True)
            return tasks

        except Exception as e:
            print(e)

    def load_modal(self):
        tasks = self.read_motivation_tasks()
        if tasks is not None:
            for key in ("sitting", "walking", "running", "continuous"):
                self.ids[key].text = tasks[key]
            self.ids.btn_save.text = "Update"

        self.open()

    def set_message(self, message):
        self.ids.task_msg.text = message

    def save_tasks(self, source, sitting, walking, running, continuous):
        userid = Session.get_user()["user_id"]
        if source == "Save":
            data = {"userid": userid, "sitting": sitting, "walking": walking, "running": running,
                    "continuous": continuous}
            if _db.save("motivation", data):
                self.set_message("tasks saved successfuly")
                self.ids.btn_save.text = "Update"
            else:
                self.set_message("failed to save tasks - try again")

        else:
            data = {"sitting": sitting, "walking": walking, "running": running, "continuous": continuous}
            if _db.update("motivation", data, f"userid='{userid}'"):
                self.set_message("motivation tasks updated successfully")
                self.ids.btn_save.text = "Update"
            else:
                self.set_message("error updating motivation task")

    def close_model(self):
        self.dismiss()
        self.ids.btn_save.text = "Save"
        self.set_message("")

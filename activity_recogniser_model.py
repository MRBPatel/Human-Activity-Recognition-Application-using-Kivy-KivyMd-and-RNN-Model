import random
from functools import partial
from threading import Thread

import numpy as np
import tensorflow as tf
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.utils import platform

# settingUp plyer to read sensor row
from plyer import accelerometer


class ActiveSensorData():
    _labels_to_be_used = ('Sitting', 'Walking', 'Running')

    """ if user is using application on smartphone def init() will enable sensor """

    @classmethod
    def init(cls):
        if platform == 'android':
            try:
                accelerometer.enable()
            except Exception as e:
                print(e)

        else:
            # set-up test row from file
            f = open("test_data.txt", "r")
            data = f.readlines()
            f.close()
            data = [i.replace(";\n", "").split(",") for i in data]
            keys = set([i[1] for i in data if len(i) == 6])
            ddata = {k: [] for k in keys}
            for i in data:
                if len(i) == 6:
                    ddata[i[1]].append(i)
            cls._data = {k: [] for k in cls._labels_to_be_used}
            for key, val in ddata.items():
                if key in cls._data.keys():
                    cls._data[key] = val.copy()

        """ When user is using SmartPhone application will collect data from sensor
         otherwise it will generate random data using numpy"""

    @classmethod
    def data_sequence(self, num_samples):
        if platform == 'android':
            try:
                inp = []
                for i in range(num_samples):
                    s = [accelerometer.acceleration[0], accelerometer.acceleration[1], accelerometer.acceleration[2]]
                    s = [float(item) for item in s]
                    inp.append(np.array(s, dtype=np.float32))
                return np.array([inp], dtype=np.float32)
            except Exception as e:
                print(e)
                return np.array([np.random.random_sample((num_samples, 3))], dtype=np.float32)

        else:
            try:
                inp = []
                key = self._labels_to_be_used[random.randint(0, 2)]
                for i in range(num_samples):
                    s = self._data[key][random.randint(0, len(self._data[key]) - 1)][3:]
                    s = [float(item) for item in s]
                    inp.append(np.array(s, dtype=np.float32))
                return np.array([inp], dtype=np.float32)
            except Exception as e:
                print(e)
                return np.array([np.random.random_sample((num_samples, 3))], dtype=np.float32)


class ActivityRecogniser():  # Loading model and analysing users activity with model
    def __init__(self) -> None:
        self._load_analyser()
        self._labels = {0: 'Sitting', 1: 'Walking', 2: 'Running'}

    def _load_analyser(self):  # Loading model in tflite format

        try:
            self._analyser = tf.lite.Interpreter(model_path="activity_recogniser_model.tflite")
            self._analyser.allocate_tensors()
            self._input_details = self._analyser.get_input_details()
            self._output_details = self._analyser.get_output_details()

        except Exception as error:
            print(error)
            self._analyser = None

    def analyse(self, data, callback):  # creating function to analyse use activity
        def job(d, calbk):
            result = None
            try:
                if self._analyser is not None:
                    self._analyser.set_tensor(self._input_details[0]['index'], d)
                    self._analyser.invoke()
                    lbls = self._analyser.get_tensor(self._output_details[0]['index'])[0]
                    cls_idx = np.argmax(np.array([lbls]))
                    result = self._labels[cls_idx]
                else:
                    print("analyser not available")

            except Exception as error:
                print(error)
            Clock.schedule_once(partial(calbk, result), 0.5)

        self._job_thread = Thread(target=job, args=(data, callback))
        self._job_thread.setDaemon(True)
        self._job_thread.start()


if __name__ == "__main__":
    def func(result, dt):
        pass


    ActiveSensorData.init()
    analyser = ActivityRecogniser()
    print(analyser.analyse(ActiveSensorData.data_sequence(90), func))
    input("_")


class PauseModel(ModalView): # creating a class  where user can pause notification when user want
    def __init__(self, _parent, **kwargs):
        super().__init__(**kwargs)
        self._parent = _parent
        self._ignore = False

    def on_option(self, value, task):
        if self._ignore:
            self._ignore = False
            return

        if value:
            keys = ["1", "3", "5"]
            t = task.split("_")[1]
            keys.remove(t)
            data = {t: self.ids[task].text}
            for key in keys:
                data[key] = ""

    def close_model(self):
        self.dismiss()

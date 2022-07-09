# module responsible for granting sensors and memory access to the app for android
from plyer.facades.accelerometer import Accelerometer
from plyer.facades.gyroscope import Gyroscope
from plyer.facades.bluetooth import Bluetooth
from kivy.utils import platform


# function to grant access for accelerometer 
def allowAccelero():
    Accelerometer.enable()


def denyAccelero():
    Accelerometer.disable()


# function to grant access for gyrometer
def allowGyro():
    Gyroscope.enable()


# function to deny gyro access
def denyGyro():
    Gyroscope.disable()


# function to grant access for external memory storage 
# Internal memory access is always allowed by default
def memoryAccess():
    if platform == "android":
        # importing python for android library
        # from that importing Permission classes
        from android.permissions import request_permissions, Permission

        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])





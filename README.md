# Human Activity Recognizer App using KivyMD

## Overview
The Human Activity Recognizer app is designed to help company employees track their movement positions during working hours. It utilizes an LSTM RNN (Long Short-Term Memory Recurrent Neural Network) model to predict four distinct user movements: Standing, Sitting, Running, and Walking. The app is built using KivyMD, a Python framework for creating cross-platform mobile applications with a modern and attractive user interface. Additionally, the app is integrated with the phone's gyroscope and accelerometer sensors to capture relevant data snippets for accurate predictions.

## Features
- Predicts user movements: The app uses a machine learning model to predict whether the user is standing, sitting, running, or walking based on sensor data.
- Real-time tracking: The app continuously monitors the user's movements and provides real-time feedback.
- User-friendly interface: KivyMD's modern and intuitive interface ensures a pleasant user experience.
- Sensor integration: The app utilizes the phone's gyroscope and accelerometer to collect data for movement prediction.
- Cross-platform compatibility: KivyMD allows the app to run on both Android and iOS devices.

## Installation
Follow these steps to install and run the Human Activity Recognizer app on your Android device:

1. Clone the repository:
   ```
   git clone https://github.com/MRBPatel/human_activity_recogniser.git
   ```

2. Navigate to the project directory:
   ```
   cd human-activity-recognizer
   ```

3. Install the required dependencies. You may need to use a virtual environment for better isolation:
   ```
   pip install -r requirements.txt
   ```

4. Run the app on your Android device:
   ```
   python main.py
   ```

## Usage
1. Upon launching the app, grant the necessary permissions for accessing the gyroscope and accelerometer sensors when prompted.

2. Place your Android device in your pocket or attach it securely to your body.

3. The app will begin monitoring your movements and providing real-time predictions on whether you are standing, sitting, running, or walking.

4. You can view your activity history and statistics within the app.



## Contributing
Contributions to this project are welcome! If you have ideas for improvements, bug fixes, or new features, please open an issue or submit a pull request.

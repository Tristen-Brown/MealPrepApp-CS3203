# Flutter + Flask Setup Guide

## Overview

I chose Flask for the backend. I've read that it is good for simple applications and is easy to integrate with Flutter. We can write our backend in Python and Flask allows it to act as an API that Flutter can call.

Besides adding a function to test whether Flutter could successfully fetch data from the backend, the starter code that Flutter came with hasn't been touched. 

## Directory Structure

### Flutter Project

The Flutter project includes:

- lib/
- ios/
- android/
- web/
- linux/
- macos/
- windows/
- test/

Most of the project's code will be in the lib/ directory. Specific files and assets are in each platform directory. These can be necessary in cases that iOS or Android need special permissions to access the user's photo library, for example. We probably don't need to worry about properly supporting desktop apps. 

The test/ directory is for tests specifically for the frontend in Flutter. 

### Backend (Flask)

The unit tests we had written previously are now in the backend/ directory. I set up Flask, which handles API calls from the FLutter app. The app.py file in backend/ handles API requests from Flutter. I wrote a simple function that returns a JSOn object that contains a string.  

The hello.dart and main.dart files in the lib/ directory show how Flutter calls the API. The hello.dart file has a fetchHello() function that shows how Flutter calls the hello function in the backend and receives the response. The fetchHello() is then called in main.dart file. I called it in the default code that came with Flutter. Basically anytime you press the button in the Flutter app it calls the fetchHello() function and prints the message in the console. 

## Setup

### Set up Flutter

***This might not work properly***

1. Visit the [Flutter SDK archive](https://docs.flutter.dev/release/archive) and download the latest SDK (version 3.24.4) for your OS and architecture. Unzip the downloaded file.

2. For Mac, you should move the unzipped file to ~/development or even just the root directory as ~/flutter. For Windows, you can move it to C:\src

3. You might need to add Flutter to your system path (PATH). I don't remember exactly how I did this. 

4. Just make sure you have the Flutter extension installed in VS Code.

5. Assuming Flutter was properly installed, in VS Code open a terminal and navigate to our app's project directory. 

6. Install Flutter dependencies by running flutter pub get. After this, VS Code might prompt you to locate the Flutter SDK. Select the directory where you placed the SDK earlier.

### Set up the backend with Flask

1. Navigate to the backend/ directory.

2. Create a virtual environment with: python -m venv venv

3. Activate the virtual environment

4. Install the dependencies for the backend with: pip install -r requirements.txt

## Running the Project

- Run the backend (Flask) server with: flask run (while in the backend/ directory)

- Run the Flutter app on a selected device with: flutter run



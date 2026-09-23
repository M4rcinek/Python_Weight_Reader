# Python based COM-data reader

A Python-based application for reading and pasting data received through a COM (serial) port.
 
## Background

This project was created as a replacement for legacy software that had been discontinued more than 10 years ago.

Over time, Windows updates and changes to the operating environment caused the original application to become unstable or stop working altogether.

## Solution

I developed a new application in Python to replace the legacy software and provide a more reliable way of communicating with the connected COM device.

The application reads data received through the serial interface, processes it, and pastes it in the place user wants in format required by Software.

## Table of Contents
1. [How does the old device work?](#1-how-does-the-old-device-work)
2. [Requirements](#2-requirements)
3. [Code Overview](#3-code-overview)

---

### 1. How does the old device work?

The original device is used to send product weight data as part of the Quality Control process.

The user presses the Send Data button on the device. The device then sends the raw weight data through the COM port in the following format:

`123.4[5] g`

---

### 2. Requirements

The new software needs to:

- Open the COM port associated with the weighing device.
- Read and process the raw weight data received from the device.
- Format the data according to the requirements of our ERP system - `123,45`.
- Automatically enter the formatted data into the field where the ERP operator has placed the cursor.

---

### 3. Code Overview

Code contains 6 different modules: `gui`, `parser`, `serial_worker`, `settings`, `tray`, `waga`.
Each module is responsible for a specific part of the application.

#### waga.py module

This module serves as the main entry point of the application. It starts the application by calling the `run_app()` method from gui module

#### parser.py module

This module contains only one method - `parse_weight()`.

What this method does is formatting the data received from the weighing device in format `123.4[5] g` to necessary `123,45` by using the regular expressions and str methods

#### serial_worker.py

The `serial_worker.py` module handles communication with the serial (COM) port.

It maps the settings selected in the GUI to the corresponding serial port parameters and opens the port for reading.
The module receives data from the weighing device, processes it using the `parse_weight()` method from `parser.py`, and automatically enters the resulting value using the keyboard library.

After entering the value, it also presses Enter. This confirms the entered value and moves the cursor to the next field, saving time when entering multiple measurements into the ERP system.

#### settings.py

Module `settings.py` is responsible for saving and loading the settings of the serial Port device(s) into the software
The settings are stored in a JSON file located in the user's AppData directory.

#### tray.py

The `tray.py` module handles minimizing the application to the system tray and creating the tray icon.
It allows the quick access to software for user to start or stop COM data reading and provides a context menu with options to terminate the application or restore the main window.

#### gui.py

This is the largest module in the application.
It builds the graphical user interface and connects the application's buttons and input fields with the functionality provided by the other modules.

The result of combining all those modules is the application with simple and easily accessible UI
<p align="center">
  <img width="301" height="241" alt="image" src="https://github.com/user-attachments/assets/9dfd52f8-6c1c-45c2-9185-abc74655a4f6" />
</p>

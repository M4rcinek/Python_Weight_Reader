import tkinter as tk
from tkinter import ttk, messagebox
from serial.tools import list_ports

from settings import load_settings, save_settings
from serial_worker import start_serial, stop_serial
import threading
from tray import create_tray

def get_com_ports():
    ports = list_ports.comports()
    return [f"{p.device} - {p.description}" for p in ports]


def run_app():
    root = tk.Tk()
    root.title("COM Weight Reader")

    frame = ttk.Frame(root, padding=10)
    frame.pack()

    settings = load_settings()

    # ---- TRAY ICON ----
    create_tray(root)

    # ---- VARS ----
    port_var = tk.StringVar(value=settings["port"])
    baud_var = tk.StringVar(value=settings["baudrate"])
    data_bits_var = tk.StringVar(value=settings["databits"])
    parity_var = tk.StringVar(value=settings["parity"])
    stop_bits_var = tk.StringVar(value=settings["stopbits"])

    status_var = tk.StringVar(value="Status: Zatrzymane")

    # ---- MENUBAR ----
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Plik", menu=file_menu)

    settings_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Ustawienia", menu=settings_menu)

    about_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="O Programie", menu=about_menu)

    file_menu.add_command(label="Minimalizuj", command=root.withdraw)
    file_menu.add_separator()
    file_menu.add_command(label="Wyjście", command=root.destroy)

    settings_menu.add_command(label="Wczytaj Ustawienia")

    about_menu.add_command(
        label="Informacje",
        command=lambda: messagebox.showinfo(
            "O Programie...",
            "Weight Reader v0.1\nAutor: Marcin Klimczyk \niCS, Colep-CP\n2026"
        )
    )

    # ---- PORT ----
    ttk.Label(frame, text="Port COM:").grid(row=0, column=0, sticky="w")
    port_combo = ttk.Combobox(frame, textvariable=port_var)
    port_combo['values'] = get_com_ports()
    port_combo.grid(row=0, column=1)

    # ---- BAUDRATE ----
    ttk.Label(frame, text="Prędkość (baudrate):").grid(row=1, column=0, sticky="w")
    baud_combo = ttk.Combobox(frame, textvariable=baud_var)
    baud_combo['values'] = ["2400","4800", "9600", "19200", "38400", "57600", "115200"]
    baud_combo.grid(row=1, column=1)

    # ---- DATA BITS ----
    ttk.Label(frame, text="Data bits:").grid(row=2, column=0, sticky="w")
    data_bits_combo = ttk.Combobox(frame, textvariable=data_bits_var)
    data_bits_combo['values'] = ["5","6","7","8"]
    data_bits_combo.grid(row=2, column=1)

    # ---- PARITY ----
    ttk.Label(frame, text="Parity:").grid(row=3, column=0, sticky="w")
    parity_combo = ttk.Combobox(frame, textvariable=parity_var)
    parity_combo['values'] = ["None","Even","Odd"]
    parity_combo.grid(row=3, column=1)

    # ---- STOP BITS ----
    ttk.Label(frame, text="Stop bits:").grid(row=4, column=0, sticky="w")
    stop_bits_combo = ttk.Combobox(frame, textvariable=stop_bits_var)
    stop_bits_combo['values'] = ["1","1.5","2"]
    stop_bits_combo.grid(row=4, column=1)

    # ---- STATUS ----
    status_label = ttk.Label(frame, textvariable=status_var)
    status_label.grid(row=6, column=0, columnspan=2)

    # ---- BUTTONS ----
    start_button = ttk.Button(frame, text="Start")
    start_button.grid(row=5, column=0, pady=10)

    stop_button = ttk.Button(frame, text="Stop", state="disabled")
    stop_button.grid(row=5, column=1, pady=10)

    # ---- CALLBACKS ----
    def log(value):
        print(value)

    def start_reading():
        port = port_var.get().split(" - ")[0]

        threading.Thread(
            target=start_serial,
            args=(
                port,
                int(baud_var.get()),
                data_bits_var.get(),
                parity_var.get(),
                stop_bits_var.get(),
                log
            ),
            daemon=True
        ).start()

        start_button.config(state="disabled")
        stop_button.config(state="normal")
        status_var.set(f"Status: Odczyt z {port}")

    def stop_reading():
        stop_serial()
        start_button.config(state="normal")
        stop_button.config(state="disabled")
        status_var.set("Status: Zatrzymane")

    start_button.config(command=start_reading)
    stop_button.config(command=stop_reading)

    # ---- SAVE ON CLOSE ----
    def on_close():
        save_settings({
            "port": port_var.get(),
            "baudrate": baud_var.get(),
            "databits": data_bits_var.get(),
            "parity": parity_var.get(),
            "stopbits": stop_bits_var.get()
        })
        root.withdraw()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
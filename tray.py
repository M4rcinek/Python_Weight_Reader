import pystray
from PIL import Image
import threading


def create_tray(root):
    def quit_app(icon, item):
        icon.stop()
        root.destroy()

    def show_window(icon, item):
        root.after(0, root.deiconify)

    def on_double_click(icon, item):
        show_window()

    image = Image.new("RGB", (64, 64), "blue")

    icon = pystray.Icon(
        "waga",
        image,
        "Weight Reader",
        menu=pystray.Menu(
            pystray.MenuItem("Pokaż", show_window),
            pystray.MenuItem("Wyjdź", quit_app)
        )
    )

    icon.on_activate = on_double_click

    threading.Thread(target=icon.run, daemon=True).start()
    return icon
import tkinter as tk

from modules.config import setup_matplotlib
from modules.gui import PoissonSimulatorApp


def main():

    setup_matplotlib()

    root = tk.Tk()

    app = PoissonSimulatorApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
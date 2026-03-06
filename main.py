import tkinter as tk
from ui import GameUI


def main():
    root = tk.Tk()
    GameUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

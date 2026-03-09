import tkinter as tk
from app import L4DConfigApp


def main():
    root = tk.Tk()
    app = L4DConfigApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
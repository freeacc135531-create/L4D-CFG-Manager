import datetime


class Logger:

    console_widget = None

    @classmethod
    def attach_console(cls, widget):
        cls.console_widget = widget

    @classmethod
    def log(cls, message):

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"

        print(line.strip())

        if cls.console_widget:
            cls.console_widget.insert("end", line)
            cls.console_widget.see("end")
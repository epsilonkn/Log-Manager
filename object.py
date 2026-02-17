from datetime import datetime
import re

class Session:

    mois_asctime = {
        "Jan": 1,"Feb": 2,"Mar": 3,"Apr": 4,"May": 5,"Jun": 6,"Jul": 7,"Aug": 8,"Sep": 9,"Oct": 10,"Nov": 11,"Dec": 12
        }

    def __init__(self, time, version):
        self.versions = version
        self.time = time

        date = re.sub(r"^[a-zA-Z]*\s", "", time)
        date = re.sub(r"\s\d{2}:\d{2}:\d{2}", "", date)
        date = re.sub(r"\s+", " ", date)

        if date : 
            self.time_obj : datetime = datetime.strptime(date, "%b %d %Y")
        else :
            self.time_obj : datetime = datetime.strptime("Jan 5 2099", "%b %d %Y") 

        self.entries : list[Entry] = []
        self.infos : list[Entry] = []
        self.warning : list[Entry] = []
        self.errors : list[Entry] = []

    def add_info(self, time, module, function, caller, message):
        info = Info(time, module, function, caller, message)
        self.entries.append(info)
        self.infos.append(info)

    def add_warning(self, time, module, function, caller, message):
        warning = Warning(time, module, function, caller, message)
        self.entries.append(warning)
        self.warning.append(warning)

    def add_error(self, time, module, function, caller, message):
        error = Error(time, module, function, caller, message)
        self.entries.append(error)
        self.errors.append(error)


class Entry:

    def __init__(self, time, module, function, caller, message):
        self.time = time
        self.module = module
        self.function = function
        self.caller = caller
        self.message : str= message
        hour = re.search(r"\d{2}:\d{2}:\d{2}", time)
        if hour :
            self.time_obj : datetime = datetime.strptime(hour.group(), "%H:%M:%S")
        else :
            self.time_obj : datetime = datetime.strptime("23:59:59", "%H:%M:%S")


    def header(self):
        return f"Entrée du {self.time} | par {self.function}, {self.module} | origine : {self.caller}"
    

    def get_message(self):
        return self.message


class Info(Entry):

    def __init__(self, time, module, function, caller, message):
        super().__init__(time, module, function, caller, message)


class Warning(Entry):

    def __init__(self, time, module, function, caller, message):
        super().__init__(time, module, function, caller, message)


class Error(Entry):

    def __init__(self, time, module, function, caller, message):
        super().__init__(time, module, function, caller, message)
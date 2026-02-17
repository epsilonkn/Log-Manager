import os
from tkinter import filedialog
import customtkinter as ct
from object import *
from pathlib import Path
from copy import deepcopy

class interface:...

class SessionsItem(ct.CTkFrame):

    def __init__(self, 
                 master, 
                 trigger = None,
                 session_object : Session = None,
                 width = 200, 
                 height = 200, 
                 corner_radius = None, 
                 border_width = None, 
                 bg_color = "transparent", 
                 fg_color = ct.ThemeManager.theme["CTkButton"]["fg_color"][ct.get_appearance_mode() == "Dark"], 
                 border_color = None, 
                 background_corner_colors = None, 
                 overwrite_preferred_drawing_method = None, 
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.bind("<Button-1>", lambda x, session = session_object : trigger(session))

        self.title = ct.CTkLabel(self, text = f"Session du {session_object.time}")
        self.version = ct.CTkLabel(self, text = f"{session_object.versions}")
        self.entries = ct.CTkLabel(self, text = f"Entrées : \
                                   infos -> {len(session_object.infos)}\
                                   warnings -> {len(session_object.warning)}\
                                   errors -> {len(session_object.errors)}")
        
        self.title.grid(column = 0, row = 0, sticky = "w", padx = 20)
        self.version.grid(column = 0, row = 1, sticky = "w", padx = 20)
        self.entries.grid(column = 0, row = 2, sticky = "w", padx = 20)



class EntryItem(ct.CTkFrame):

    def __init__(self, 
                 master, 
                 trigger = None,
                 entry_object : Entry = None,
                 width = 200, 
                 height = 200, 
                 corner_radius = None, 
                 border_width = None, 
                 bg_color = "transparent", 
                 border_color = None, 
                 background_corner_colors = None, 
                 overwrite_preferred_drawing_method = None, 
                 **kwargs):
        
        colors = {Info : "#00DA7F", Warning :"#FF8800", Error : "#FF3333"}
        fg_color = colors.get(entry_object.__class__)
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)


        text = ct.CTkLabel(self, text = entry_object.header(), anchor="w", compound = "left", text_color= "#FFFFFF")
        text.grid(row = 0, column = 0, padx = 10, sticky = "w")

        text = ct.CTkLabel(self, text = entry_object.get_message(), anchor="w", compound = "left", text_color= "#FFFFFF", wraplength=900)
        text.grid(row = 1, column = 0, padx = 10, sticky = "w")


class Sorter:

    @staticmethod
    def sortErrorDecreasing(view : list[Session]):
        for i in range(1, len(view)):
            y = i
            while y > 0 and len(view[y].errors) > len(view[y-1].errors) :
                view[y], view[y-1] = view[y-1], view[y]
                y -= 1
        return view


    @staticmethod
    def sortWarningDecreasing(view : list[Session]):
        for i in range(1, len(view)):
            y = i
            while y > 0 and len(view[y].warning) > len(view[y-1].warning) :
                view[y], view[y-1] = view[y-1], view[y]
                y -= 1
        return view


    @staticmethod
    def sortInfoDecreasing(view : list[Session]):
        for i in range(1, len(view)):
            y = i
            while y > 0 and len(view[y].infos) > len(view[y-1].infos) :
                view[y], view[y-1] = view[y-1], view[y]
                y -= 1
        return view
    

    @staticmethod
    def sortErrorIncreasing(view : list[Session]):
        for i in range(1, len(view)):
            y = i
            while y > 0 and len(view[y].errors) < len(view[y-1].errors) :
                view[y], view[y-1] = view[y-1], view[y]
                y -= 1
        return view
    

    @staticmethod
    def sortWarningIncreasing(view : list[Session]):
        for i in range(1, len(view)):
            y = i
            while y > 0 and len(view[y].warning) < len(view[y-1].warning) :
                view[y], view[y-1] = view[y-1], view[y]
                y -= 1
        return view
    

    @staticmethod
    def sortInfoIncreasing(view : list[Session]):
        for i in range(1, len(view)):
            y = i
            while y > 0 and len(view[y].infos) < len(view[y-1].infos) :
                view[y], view[y-1] = view[y-1], view[y]
                y -= 1
        return view
    
    @staticmethod
    def sortByDate(view : list[Session]):
        for i in range(1, len(view)):
            y = i
            while y > 0 and view[y].time_obj > view[y-1].time_obj :
                view[y], view[y-1] = view[y-1], view[y]
                y -= 1
        return view
    


class interface(ct.CTk):

    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.geometry("1200x800")
        self.title("Log reader")

        self.logFilePath : Path | None = None
        self.logFileName : str = ""

        self.sessions : list[Session] = []
        self.sessions_view : list[Session] = []

        if not self.logFilePath :
            self.search_frame()
        else :
            self.overview()


    def clear(self, entity = None):
        if not entity : entity = self
        for elt in entity.pack_slaves() + entity.grid_slaves() + entity.place_slaves():
            if isinstance(elt, (ct.CTkFrame, ct.CTkScrollableFrame)):
                self.clear(elt)
            elt.destroy()


    def search_frame(self):
        self.clear()
        self.bt = ct.CTkButton(self, width=200, height=100, text="ouvrir un fichier", command=self.choose_log)
        self.bt.place(x = 500, y = 350)


    def choose_log(self):
        path = filedialog.askopenfilename(
            filetypes=[("Fichier de Log", "*.log")],
            title="Enregistrer sous",
            initialdir=os.getcwd()
        )
        if ".log" in path :
            self.logFilePath = Path(path)
            self.logFileName = self.logFilePath.stem
            self.overview()
        


    def overview(self):    
        self.clear()
        self.title = ct.CTkLabel(self, text = f"Liste des entrées de : {self.logFileName}",
                                 font= ct.CTkFont("arial", size = 30, weight="bold"))
        
        self.dashboard = ct.CTkScrollableFrame(self, 1100, 200)
        self.dashboard.grid_columnconfigure(0, weight=1)
        self.dashboard.grid_columnconfigure(1, weight=1)
        self.dashboard.grid_columnconfigure(2, weight=1)

        self.option_f = ct.CTkFrame(self, width=1100)

        self.listframe = ct.CTkScrollableFrame(self, 1100, 500)
        self.listframe.grid_columnconfigure(0, weight=1)

        self.title.pack(pady = 10)
        self.dashboard.pack()
        self.option_f.pack()
        self.listframe.pack()

        #---------------option_f ----------------------------

        sort_info = ct.CTkOptionMenu(self.option_f)

        self.list_sessions(self.sessions)
        self.create_dashboard()


    def session_detail(self, session : Session):
        self.clear()
        top = ct.CTkFrame(self, 1100, 50)
        event_f = ct.CTkScrollableFrame(self, 1100, 700, label_text=f"{len(session.infos) + len(session.warning) + len(session.errors)} Events")

        top.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew', padx = 40) 
        event_f.grid(row = 1, column = 0, padx = [40, 0], sticky = 'nsew') 

        return_bt = ct.CTkButton(top, text = "Retour", command=self.overview)
        session_text = ct.CTkLabel(top, text = f"Session du {session.time}")

        return_bt.grid(row = 0, column = 0, padx = 10, pady = 5)
        session_text.grid(row = 0, column = 1, padx = 10, pady = 5)

        for i, entry in enumerate(session.entries) :
            f = EntryItem(event_f, width = 900, entry_object = entry, corner_radius = 10)
            f.grid(row = i, column = 0, sticky = 'nsew', pady = 5, ipady = 5)


    def list_sessions(self, session_list : list = []):
        """
        function that lists all the sessions parsed in the log file
        """
        if session_list == [] :
            sessions = self.parse_log()
        else : sessions = session_list
        for i, session in enumerate(sessions):
            SessionsItem(self.listframe, self.session_detail, session).grid(row = i, column = 0, sticky = 'nsew', pady = 5, padx = 10)

    
    def create_dashboard(self):
        types = ["infos", "warning", "errors"]
        colors = ["#00DA7F", "#FF8800", "#FF3333"]
        for i, elt in enumerate(types) :
            f = ct.CTkFrame(self.dashboard, width=300, height=150)
            title = ct.CTkLabel(f, text = elt + " :", font=ct.CTkFont(family="arial", size = 30, weight= "bold"))
            nb = ct.CTkLabel(f, text = self._get_entries_nb(elt), 
                             font=ct.CTkFont(family="arial", size = 40, weight= "bold"),
                             text_color=colors[i])

            f.grid(row = 0, column = i, sticky = 'nsew', padx = 25, pady = 25)
            title.pack(pady = 20)
            nb .pack(pady = 20)

        
    def _get_entries_nb(self, mod):
        match mod:

            case 'infos':
                return sum([len(ses.infos) for ses in self.sessions])
            case 'warning':
                return sum([len(ses.warning) for ses in self.sessions])
            case 'errors':
                return sum([len(ses.errors) for ses in self.sessions])


    def list_entries(self, session_str : str, session_obj : Session):
        """
        lists all the infos parsed in a session
        """

        def create_entry(start, end, entry_type):
            cut = session_str[start:end]
            time = cut[cut.index("<timestamp>"):cut.index("</timestamp>")].replace("<timestamp>", "")
            module = cut[cut.index("<module>"):cut.index("</module>")].replace("<module>", "")
            function = cut[cut.index("<function>"):cut.index("</function>")].replace("<function>", "")
            caller = cut[cut.index("<caller>"):cut.index("</caller>")].replace("<caller>", "")
            message = cut[cut.index("<message>"):cut.index("</message>")].replace("<message>", "")

            match entry_type :
                    case 'info':
                        session_obj.add_info(time, module, function, caller, message)
                    case 'warning':
                        session_obj.add_warning(time, module, function, caller, message)
                    case 'error':
                        session_obj.add_error(time, module, function, caller, message)


        pointer = 0
        while pointer < len(session_str) :
            if session_str[pointer] == "<" :
                end_point = pointer + 1
                if session_str.find("<info>", pointer) == pointer :
                    end_point = session_str.find("</info>", pointer)
                    create_entry(pointer, end_point, "info")
                elif session_str.find("<warning>", pointer) == pointer :
                    end_point = session_str.find("</warning>", pointer)
                    create_entry(pointer, end_point, "warning")

                elif session_str.find("<error>", pointer) == pointer :
                    end_point = session_str.find("</error>", pointer)
                    create_entry(pointer, end_point, "error")

                pointer = end_point
            else :
                pointer += 1

    def parse_log(self):
        session_list = []
        raw_log = self.open_log(self.logFilePath)
        for sessions in raw_log.split("<login>"):
            if "<init>" not in sessions :
                continue
            init = sessions[sessions.index("<init>"):sessions.index("</init>")]
            time = init[init.index("<timestamp>"):init.index("</timestamp>")].replace("<timestamp>", "")
            version = init[init.index("<version>"):init.index("</version>")].replace("<version>", "")
            session = Session(time, version)
            self.list_entries(sessions, session)
            session_list.append(session)
        self.sessions = session_list
        return session_list



    def open_log(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
        

if __name__ == "__main__":
    win = interface()
    win.mainloop()
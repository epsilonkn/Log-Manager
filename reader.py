import os
from tkinter import filedialog
import customtkinter as ct
from object import *
from pathlib import Path

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

        


class interface(ct.CTk):

    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.geometry("1400x800")
        self.title("Log reader")

        self.logFilePath : Path | None = None
        self.logFileName : str = ""

        self.sessions : list[Session] = []

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
        self.bt.place(x = 600, y = 350)


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

        self.listframe = ct.CTkScrollableFrame(self, 1300, 500)
        self.listframe.grid_columnconfigure(0, weight=1)

        self.dashboard = ct.CTkScrollableFrame(self, 1300, 200)
        self.dashboard.grid_columnconfigure(0, weight=1)
        self.dashboard.grid_columnconfigure(1, weight=1)
        self.dashboard.grid_columnconfigure(2, weight=1)

        self.title.pack(pady = 10)
        self.dashboard.pack()
        self.listframe.pack()

        self.list_sessions()
        self.create_dashboard()


    def session_detail(self, session : Session):
        self.clear()
        top = ct.CTkFrame(self, 1300, 50)
        info_f = ct.CTkScrollableFrame(self, 650, 300, label_text=f"{len(session.infos)} Infos")
        warning_f = ct.CTkScrollableFrame(self, 650, 300, label_text=f"{len(session.warning)} Warning")
        error_f = ct.CTkScrollableFrame(self, 1300, 350, label_text=f"{len(session.errors)} Errors")

        top.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew', padx = 40) 
        info_f.grid(row = 1, column = 0, padx = [40, 0], sticky = 'nsew') 
        warning_f.grid(row = 1, column = 1, padx = [0, 40], sticky = 'nsew') 
        error_f.grid(row = 2, column = 0, columnspan = 2, padx = 40) 


        return_bt = ct.CTkButton(top, text = "Retour", command=self.overview)
        session_text = ct.CTkLabel(top, text = f"Session du {session.time}")

        return_bt.grid(row = 0, column = 0, padx = 10, pady = 5)
        session_text.grid(row = 0, column = 1, padx = 10, pady = 5)

        for i, info in enumerate(session.infos) :
            f = ct.CTkFrame(info_f, 450, fg_color=ct.ThemeManager.theme["CTkButton"]["fg_color"][ct.get_appearance_mode() == "Dark"], corner_radius = 10)
            f.grid(row = i, column = 1, sticky = 'nsew', pady = 5, ipady = 5)
            text = ct.CTkLabel(f, text = info.__str__(), anchor="w", compound = "left", text_color= "#FFFFFF")
            text.pack(padx = 10)

        for warning in session.warning :
            pass

        for error in session.errors:
            pass



    def list_sessions(self):
        """
        function that lists all the sessions parsed in the log file
        """
        if self.sessions == [] :
            sessions = self.parse_log()
        else : sessions = self.sessions
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


    def list_entries(self, session_str : str, session_obj : Session, entry_type : str):
        """
        lists all the infos parsed in a session
        """
        start_point = 0
        end_point = 0
        while end_point != -1 :
            start_point = session_str.find(f"<{entry_type}>", end_point)
            end_point = session_str.find(f"</{entry_type}>", start_point)
            if end_point != -1 :
                cut = session_str[start_point:end_point]
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
            self.list_entries(sessions, session, 'info')
            self.list_entries(sessions, session, 'error')
            self.list_entries(sessions, session, 'warning')
            session_list.append(session)
        self.sessions = session_list
        return session_list



    def open_log(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
        

if __name__ == "__main__":
    win = interface()
    win.mainloop()
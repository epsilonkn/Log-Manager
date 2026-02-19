import os
import time


class LogNotInstanciatedError(BaseException):
    pass


class Log:

    __version__ = 1.0

    _instance = None


    def __init__(self, cwd_path : str = "./", log_name : str = "module.log"):
        """
        Constructeur de la classe log, n'est pas fait pour être lancé directement.
        Pour ouvrir le log, utilisez la méthode "start_log"

        Args:
            cwd_path (str, optional): chemin vers le dossier devant contenir le log. Defaults to "./".
            log_name (str, optional): Nom du fichier de Logs. Defaults to "module.log".
        """

        self.path = cwd_path
        self.opened = False
        if log_name in os.listdir(cwd_path) :
            self.f = os.path.join(cwd_path, log_name)
        else : 
            f = open(os.path.join(cwd_path, log_name), 'w')
            f.close()
            self.f = os.path.join(cwd_path, log_name)
    

    @classmethod
    def start_log(cls, cwd : str = "./", log_name : str = "module.log", module_version : float = -1):
        """
        méthode d'ouverture du log

        Args:
            cwd (str, optional): chemin vers le dossier devant contenir le log. Defaults to "./".
            log_name (str, optional): Nom du fichier de Logs. Defaults to "module.log".
            module_version (float, optional): Version du module appelant le Log. Defaults to -1.
        """
        if not cls._instance :
            cls._instance = Log(cwd, log_name)
        if not cls._instance.opened :
            init = "\n<login>"
            detail =  f"\n\t<init>\
                        \n\t\t<timestamp>{time.asctime()}</timestamp>\
                        \n\t\t<version>log version :{cls.__version__}, module version : {module_version}</version>\
                        \n\t</init>"
            init += detail
            cls._write_in_log(init)



    @classmethod
    def close_log(cls):
        """
        Ferme le log à l'appel du module l'ayant ouvert

        Raises:
            LogNotInstanciatedError: Erreur renvoyée si le Log n'a pas été ouvert avant fermeture
        """
        if not cls._instance :
            raise LogNotInstanciatedError("Le log n'a pas été ouvert, fermeture impossible")
        else :
            cls._write_in_log("\n</login>")


    @classmethod
    def _write_in_log(cls, message : str):
        """
        Méthode d'écriture dans le log, 
        appelée uniquement par les méthodes d'ajout d'une entrée

        Args:
            message (str): message à écrire dans le log
        """
        with open(cls._instance.f, 'a', encoding='utf-8') as f :
            f.writelines(message)


    @classmethod
    def error(cls, 
                error : BaseException, 
                addon : str = "",
                timestamp : bool = True,
                module_name : str = "unknown",
                function : str = "unknown",
                caller : str = "module"
              ) -> None:
        """
        Ecrit une erreur dans le log

        Args:
            error (BaseException): erreur renvoyée par le module appelant
            addon (str, optional): message complémentaire précisant l'erreur. Defaults to "".
            timestamp (bool, optional): horodatage de l'entrée. Defaults to True.
            module_name (str, optional): nom du module appelant la méthode. Defaults to "unknown".
            function (str, optional): nom de la fonction appelant la méthode. Defaults to "unknown".
            caller (str, optional): nom de l'entité appelant la méthode. Defaults to "module".

        Example:

            erreur envoyée par la fonction main d'un fichier script.py :
            error(Exception("example"), "this is an add-on", module_name="script.py", function="main", caller="module")

            erreur envoyée par le developpeur du module script.py dans la fonction main :
            error(Exception("example"), "this action is prohibited", module_name="script.py", function="main", caller="dev")


        """
        message = "\n\t<error>"
        message += f"\n\t\t<timestamp>{time.asctime()}</timestamp>" if timestamp else ""
        message += f"\n\t\t<module>{module_name}</module><function>{function}</function><caller>{caller}</caller>"
        message += f"\n\t\t<message>line {error.__traceback__.tb_lineno}, {error.__str__()}, {addon}</message>"
        message += "\n\t</error>"

        cls._write_in_log(message)


    @classmethod
    def info(cls, 
            *input : str, 
             timestamp : bool = True,
             module_name : str = "unknown",
             function : str = "unknown",
             caller : str = "module",
             tag : str | None = None
             ) -> None:
        """
        Methode d'écriture d'une information ou plusieurs dans le log

        Args:
            *input (str): messages à écrire dans le log, il peut y en avoir plusieurs à la suite
            timestamp (bool, optional): horodatage de l'entrée. Defaults to True.
            module_name (str, optional): nom du module appelant la méthode. Defaults to "unknown".
            function (str, optional): nom de la fonction appelant la méthode. Defaults to "unknown".
            caller (str, optional): nom de l'entité appelant la méthode. Defaults to "module".
            tag (str | None, optional): tag precisant le type de message, peut être "resultat", "operation", "reponse". Defaults to None.
        """
        addtag = f" tag={tag}" if tag else ""
        message = f"\n\t<info{addtag}>"
        message += f"\n\t\t<timestamp>{time.asctime()}</timestamp>" if timestamp else ""
        message += f"\n\t\t<module>{module_name}</module><function>{function}</function><caller>{caller}</caller>"
        message += "\n\t\t<message>"
        for msg in input :
            message += (str(msg) + "\n\t\t")
        message += "</message>\n\t</info>"
        cls._write_in_log(message)


    @classmethod
    def warning(cls, 
                warning_message : str = "",
                timestamp : bool = True,
                module_name : str = "unknown",
                function : str = "unknown",
                caller : str = "module"
              ) -> None:
        """
        Méthode d'écriture d'un warning dans le log

        Args:
            warning_message (str, optional): Warning à écrire dans le log. Defaults to "".
            timestamp (bool, optional): horodatage de l'entrée. Defaults to True.
            module_name (str, optional): nom du module appelant la méthode. Defaults to "unknown".
            function (str, optional): nom de la fonction appelant la méthode. Defaults to "unknown".
            caller (str, optional): nom de l'entité appelant la méthode. Defaults to "module".
        """
        message = "\n\t<warning>"
        message += f"\n\t\t<timestamp>{time.asctime()}</timestamp>" if timestamp else ""
        message += f"\n\t\t<module>{module_name}</module><function>{function}</function><caller>{caller}</caller>"
        message += f"\n\t\t<message>{warning_message}</message>"
        message += "\n\t</warning>"

        cls._write_in_log(message)
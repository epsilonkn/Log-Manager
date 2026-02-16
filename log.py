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
        if not cls._instance :
            raise LogNotInstanciatedError("Le log n'a pas été ouvert, fermeture impossible")
        else :
            cls._write_in_log("\n</login>")


    @classmethod
    def _write_in_log(cls, message):
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
        message = "\n\t<warning>"
        message += f"\n\t\t<timestamp>{time.asctime()}</timestamp>" if timestamp else ""
        message += f"\n\t\t<module>{module_name}</module><function>{function}</function><caller>{caller}</caller>"
        message += f"\n\t\t<message>{warning_message}</message>"
        message += "\n\t</warning>"

        cls._write_in_log(message)


if __name__ == "__main__" :

    Log.start_log(module_version=2)
    Log.info("ceci est un message", "c'en est un autre", module_name="test.py", function="main", caller="admin")
    Log.info("encore un autre message", module_name="test.py", function="main", caller="admin", tag = "default")
    try : 
        raise Exception("ceci est une erreur au pif")
    except Exception as e :
        Log.error(e, module_name="test.py", function="main", caller="sys")
    Log.close_log()

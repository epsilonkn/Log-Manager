

class Session:

    def __init__(self, time, version):
        self.versions = version
        self.time = time
        self.infos = []
        self.warning = []
        self.errors = []

    def add_info(self, time, module, function, caller, message):
        info = Info(time, module, function, caller, message)
        self.infos.append(info)

    def add_warning(self, time, module, function, caller, message):
        info = Warning(time, module, function, caller, message)
        self.warning.append(info)

    def add_error(self, time, module, function, caller, message):
        info = Error(time, module, function, caller, message)
        self.errors.append(info)


class Info:

    def __init__(self, time, module, function, caller, message):
        self.time = time
        self.module = module
        self.function = function
        self.caller = caller
        self.message = message


class Warning:

    def __init__(self, time, module, function, caller, message):
        self.time = time
        self.module = module
        self.function = function
        self.caller = caller
        self.message = message


class Error:

    def __init__(self, time, module, function, caller, message):
        self.time = time
        self.module = module
        self.function = function
        self.caller = caller
        self.message = message
from configparser import ConfigParser
from graphicInterface.console import Logger


class RegistrationParameters:

    instance = None

    class __PrivateParams:  # Singleton

        def __init__(self):
            c = ConfigParser()
            c.read('registration_parameters.conf')
            ps = c['PARAMETERS']
            # Now read every key
            self.tolerance = float(ps['tolerance'])
            self.max_iterations = int(ps['max_iterations'])
            self.sigma2 = None if ps['sigma2'] == 'None' else float(ps['sigma2'])
            self.w = float(ps['w'])
            self.params = {'tolerance': self.tolerance,
                           'max_iterations': self.max_iterations,
                           'sigma2': self.sigma2,
                           'w': self.w}

        def get_param(self, key):
            try:
                return self.params[key]
            except KeyError:
                return None

        def write_on_file(self):
            with open('registration_parameters.conf', 'w+') as conf_file:
                conf = ConfigParser()
                conf['PARAMETERS'] = {}
                for key, value in self.params.items():
                    conf['PARAMETERS'][str(key)] = str(value)
                conf.write(conf_file)
                Logger.addRow("Configuration file updated")

        def get_params(self):
            return self.params

        def set_params(self, key, value):
            self.params[key] = value

    def __init__(self):
        if RegistrationParameters.instance is None:
            RegistrationParameters.instance = self.__PrivateParams()

    @staticmethod
    def get_params():
        """ Returns a dictionary with all the registration parameters. """
        return RegistrationParameters.instance.get_params()

    @staticmethod
    def get_param(key):
        return RegistrationParameters.instance.get_param(key)

    @staticmethod
    def set_param(key, value):
        RegistrationParameters.instance.set_params(key, value)

    @staticmethod
    def write_on_file():
        RegistrationParameters.instance.write_on_file()

    def to_string(self):
        param = self.get_params()
        ss = ""
        for k in param:
            ss += k + " : " + str(param[k]) + " | "

        return ss[0:-2]


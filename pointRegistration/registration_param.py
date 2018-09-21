from configparser import ConfigParser


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

        def getParams(self):
            param = {'tolerance':  self.tolerance,
                     'max_iterations': self.max_iterations,
                     'sigma2': self.sigma2,
                     'w': self.w}
            return param

    def __init__(self):
        if RegistrationParameters.instance is None:
            RegistrationParameters.instance = self.__PrivateParams()

    def getParams(self):
        """ Returns a dictionary with all the registration parameteres. """
        return RegistrationParameters.instance.getParams()

    def to_string(self):
        param = self.getParams()
        ss = ""
        for k in param:
            ss += k + " : " + str(param[k]) + " | "

        return ss[0:-2]


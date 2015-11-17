import abc

class IQuerier(object):
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def identify(self, geometry, layers, url, username, password):
         """Method that should do something."""

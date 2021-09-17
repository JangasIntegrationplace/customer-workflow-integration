from abc import ABC, abstractclassmethod, abstractproperty


class BaseHandler(ABC):
    @abstractproperty
    def query_language_mapper(self):
        pass

    @abstractclassmethod
    def create_initial_input(cls, data: dict):
        """
        Stores initial input into database.
        """
        pass

    @abstractclassmethod
    def create_output_stream(cls, data: dict):
        """
        Stores fully proceed data into database.
        """
        pass

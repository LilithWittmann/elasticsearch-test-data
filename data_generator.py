import abc
import json
import random
import string
import sys

from faker import Factory


class ValueGenerator(object):

    __metaclass__ = abc.ABCMeta

    value_type = None # the value type e.g. string, integer
    allowed_attributes = None

    faker = None

    def __init__(self):
        self.faker = Factory.create()

    @abc.abstractmethod
    def generate(self, definition):
        pass


    def _choose_option(self, options):
        """select a random option from a list

            :Parameters:
                - `options` - list of options

            :Returns:
                an option
        """
        choice = random.randrange(0, len(options))
        return options[choice]


class StringGenerator(ValueGenerator):

    value_type = "string"
    allowed_attributes = ["min_length", "max_length", "options"]

    def __init__(self):
        super(StringGenerator, self).__init__()


    def generate(self, settings):
        """Generate a string with a min and max length 
           or choose a string from a list

            :Parameters:
                - `settings` - dict of options

            :Returns:
                - a string

            :Options:
                - `min_length` - minimum string length
                - `max_length` - maxium string length
                - `options` - list of strings (if options is set min_length and max_length will be ignored)
                - `content` - kind of text content (currently random, text, name, address)
        """

        if "options" in settings:
            return self._choose_option(settings["options"])

        if "min_length" in settings:
            min_length = settings["min_length"]
        else:
            min_length = 0

        if "max_length" in settings:
            max_length = settings["max_length"]
        else:
            max_length = 9999999

        if "content" not in settings or settings["content"] is "random":
            length = random.randrange(min_length, max_length)
            return "".join([random.choice(string.ascii_letters + string.digits) for x in range(length)])

        elif settings["content"] is "text":
            text = self.faker.text()
            if len(text) > max_length:
                text = text[:max_length]

            if min_length > len(text):
                while min_length > len(text):
                    text = "{} {}".format(text, self.faker.text())
            return text

        elif settings["content"] is "name":
            return self.faker.name()

        elif settings["content"] is "address":
            return self.faker.address()


        #TODO(lilith) implement more content types

class IntegerGenerator(ValueGenerator):
    """Generate an integer with a min and max length 
       or choose an integer from a list of possible integers

    :Parameters:
        - `settings` - dict of options

    :Returns:
        - an integer

    :Options:
        - `min` - min integer
        - `max` - max integer
        - `options` - list of possible integers

    """
    value_type = "integer"
    allowed_attributes = ["min", "max", "options"]

    def __init__(self):
        super(IntegerGenerator, self).__init__()

    def generate(self, settings):

        if "options" in settings:
            return self._choose_option(settings["options"])

        if "min" in settings:
            min_int = settings["min"]
        else:
            min_int = sys.minint

        if "max" in settings:
            min_int = settings["max"]
        else:
            min_int = sys.maxint

        return random.randrange(min_int, max_int)

class FloatGenerator(ValueGenerator):

    value_type = "integer"
    allowed_attributes = ["min", "max", "options"]

    def __init__(self):
        super(FloatGenerator, self).__init__()

    def generate(self, settings):
        if "options" in settings:
            return self._choose_option(settings["options"])

        return random.uniform(1.5, 1.9)
        

class DateGenerator(ValueGenerator):

    value_type = "date"
    allowed_attributes = ["min_date", "max_date", "options"]

    def __init__(self):
        super(DateGenerator, self).__init__()
        
    def generate(self, settings):

        if "options" in settings:
            return self._choose_option(settings["options"])
            
        if "min_date" in settings:
            min_date = settings["min_date"]

        if "max_date" in settings:
            min_date = settings["min_date"]



        fake.date_time_between(start_date="-30y", end_date="now")



PARSER_MAPPING = {

    StringGenerator.value_type: StringGenerator,
    IntegerGenerator.value_type: IntegerGenerator,
    FloatGenerator.value_type: FloatGenerator,
    DateGenerator.value_type: DateGenerator

}


class DataGenerator(object):

    def __init__(self, format_definition):
        """Generate Test Data from json format_definition

            :Parameters:
                - format_definition - A dict or string with the format definition
        """
        if type(json) == str:
            self.format_definition = json.loads(data)
        else:
            self.format_definition = data


    def generate(self):
        """generate the example data"""
        pass

    def validate(self):
        """validate a data schema"""
        pass

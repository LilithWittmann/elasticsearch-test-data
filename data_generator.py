import abc
from datetime import datetime
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
    """Generate an integer with a min and max value 
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
        """Generate a date (delimited by min und max date)
           or choose a date from a list of possible dates

        :Parameters:
            - `settings` - dict of options

        :Returns:
            - a datetime

        :Options:
            - `min` - min date (e.g iso date or -10d or now)
            - `max` - max date (e.g. iso date or 100y or now)
            - `options` - list of possible integers

        """

        if "options" in settings:
            return self._choose_option(settings["options"])

        if "min_date" in settings:
            min_date = settings["min_date"]
        else:
            min_date = "-100y"

        if "max_date" in settings:
            max_date = settings["max_date"]
        else:
            max_date = "now"


        return self.faker.date_time_between(start_date=min_date, end_date=max_date)
        

class DictGenerator(ValueGenerator):

    value_type = "dict"
    allowed_attributes = []

    def __init__(self):
        super(DictGenerator, self).__init__()
        
    def generate(self, input_dict):
        """Generate a dict (from a dict)

        :Parameters:
            - `input_dict` - dict

        :Returns:
            - a dict

        """

        result_data = {}

        # iterate over all dict fields
        for key, value in input_dict.items():
            # get generatpr from generators list
            if type(value) is dict and "type" in value and value["type"] is not None \
                and value["type"] in GENERATOR_MAPPING:

                generator = GENERATOR_MAPPING[value["type"]]
                generator_instance = generator()
                # generate the value
                result_data[key] = generator_instance.generate(value)
            elif type(value) is dict and "type" not in value:
                result_data[key] = self.generate(value)
            else:
                raise Exception("Generator '{}' not found".format(value["type"]))

        return result_data



GENERATOR_MAPPING = {

    StringGenerator.value_type: StringGenerator,
    IntegerGenerator.value_type: IntegerGenerator,
    FloatGenerator.value_type: FloatGenerator,
    DateGenerator.value_type: DateGenerator,
    DictGenerator.value_type: DictGenerator

}





class DataGenerator(object):

    def __init__(self, format_definition):
        """Generate Test Data from json format_definition

            :Parameters:
                - format_definition - A dict or string with the format definition
        """
        if type(json) == str:
            self.format_definition = json.loads(format_definition)
        else:
            self.format_definition = format_definition


    def generate(self):
        """generate the example data"""
        
        dict_generator = DictGenerator()
        return dict_generator.generate(self.format_definition)




    def validate(self):
        """validate a data schema"""
        pass

import itertools


class DataService(object):

    @staticmethod
    def iter_prompt(data_dict_it, prompt, parse_fields_func):
        """ This method composes prompt from the multiple fields, mentioned in it.
            data_it: Iterator
                iterator of the dict, from which we can collect data.
        """
        assert(callable(parse_fields_func))
        field_names = list(parse_fields_func(prompt))
        for data_dict in data_dict_it:
            assert(isinstance(data_dict, dict))
            field_contents = [([data_dict[field_name]] if isinstance(data_dict[field_name], str) else data_dict[field_name])
                              if isinstance(field_name, str) else field_name
                              for field_name in field_names]
            yield list(itertools.chain(*field_contents))

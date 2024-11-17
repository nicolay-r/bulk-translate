class DataService(object):

    @staticmethod
    def iter_prompt(data_dict_it, prompt, parse_fields_func):
        """ This method composes prompt from the multiple fields, mentioned in it.
            data_it: Iterator
                iterator of the dict, from which we can collect data.
        """
        assert(callable(parse_fields_func))
        field_names = list(parse_fields_func(prompt))
        for row_id, data_dict in enumerate(data_dict_it):
            assert(isinstance(data_dict, dict))
            fmt_d = {col_name: data_dict[col_name] for col_name in field_names}
            yield row_id, prompt.format(**fmt_d)
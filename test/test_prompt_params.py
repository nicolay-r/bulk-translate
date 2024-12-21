import unittest

from bulk_translate.src.service_prompt import DataService
from bulk_translate.src.utils import iter_params


class TestIterPromptParameters(unittest.TestCase):

    def test(self):
        data_it = DataService.iter_prompt(
            data_dict_it=[{"t": ["111", ["SDFSDFSD"]], "p": [["Q"], "222"], "q": ["333", ["Z"], "2312"]}],
            prompt="o {t} XXX yyy ZZZ {p} aaa {q} t",
            parse_fields_func=iter_params)

        for u in data_it:
            print(u)
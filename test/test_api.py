import json
import unittest
from os.path import dirname, realpath, join

from bulk_translate.api import Translator
from bulk_translate.src.service_dynamic import dynamic_init


class TestTranslatorPipeline(unittest.TestCase):
    text = ["C'était en",  ["juillet 1805"] , "et l'oratrice était la célèbre", ["Anna Pavlovna"]]

    CURRENT_DIR = dirname(realpath(__file__))

    def test_benchmark(self):
        translation_model = dynamic_init(src_dir=join(TestTranslatorPipeline.CURRENT_DIR, "../models"),
                                         class_filepath="googletrans_310a.py",
                                         class_name="GoogleTranslateModel")()

        translator = Translator(translate_spans=False,
                                translation_model=translation_model,
                                # custom args
                                src="auto",
                                dest="en")

        content = [
            {"text": TestTranslatorPipeline.text}
        ]

        data_it = translator.iter_translated_data(
            data_dict_it=iter(content),
            schema=json.loads('{"translated":"{text}"}')
        )

        for d in data_it:
            print(d)

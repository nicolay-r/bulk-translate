import unittest
from os.path import dirname, realpath, join

from arekit.common.entities.base import Entity
from arekit.common.pipeline.batching import BatchingPipelineLauncher
from arekit.common.pipeline.context import PipelineContext
from arekit.contrib.utils.pipelines.items.text.entities_default import TextEntitiesParser

from bulk_translate.src.pipeline.translator import MLTextTranslatorPipelineItem
from bulk_translate.src.service_dynamic import dynamic_init


class TestTranslatorPipeline(unittest.TestCase):
    text = "C'était en [juillet_1805] , et l'oratrice était la célèbre [Anna_Pavlovna]"

    CURRENT_DIR = dirname(realpath(__file__))

    def test_benchmark(self):
        translation_model = dynamic_init(src_dir=join(TestTranslatorPipeline.CURRENT_DIR, "../models"),
                                         class_filepath="googletrans_310a.py",
                                         class_name="GoogleTranslateModel")()

        pipeline = [
            TextEntitiesParser(src_func=lambda text: text.split()),
            MLTextTranslatorPipelineItem(batch_translate_model=translation_model.get_func(src="auto", dest="en"),
                                         do_translate_entity=False),
        ]

        ctx = PipelineContext(d={"input": [TestTranslatorPipeline.text]})

        BatchingPipelineLauncher.run(pipeline=pipeline, pipeline_ctx=ctx, src_key="input")
        print([[item.DisplayValue] if isinstance(item, Entity) else item
               for item in ctx.provide("result")[0]])

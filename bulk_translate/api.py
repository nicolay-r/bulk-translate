from bulk_translate.src.pipeline.context import PipelineContext
from bulk_translate.src.pipeline.items.base import BasePipelineItem
from bulk_translate.src.pipeline.items.map import MapPipelineItem
from bulk_translate.src.pipeline.launcher import BatchingPipelineLauncher
from bulk_translate.src.pipeline.translator import MLTextTranslatorPipelineItem
from bulk_translate.src.pipeline.utils import BatchIterator
from bulk_translate.src.service_prompt import DataService
from bulk_translate.src.span import Span
from bulk_translate.src.spans_parser import TextSpansParser
from bulk_translate.src.utils import iter_params


class Translator(object):

    def __init__(self, translate_spans, translation_model, **custom_args_dict):
        self.pipeline = [
            TextSpansParser(src_func=lambda text: [text] if isinstance(text, str) else text),
            MLTextTranslatorPipelineItem(
                batch_translate_model=translation_model.get_func(**custom_args_dict),
                do_translate_entity=translate_spans),
            MapPipelineItem(map_func=lambda term:
                ([term.DisplayValue] + ([term.content] if term.content is not None else []))
                if isinstance(term, Span) else term),
            BasePipelineItem(src_func=lambda src: list(src))
        ]

    def iter_translated_data(self, data_dict_it, prompt, batch_size=1):
        """ This is the main API method for calling.
        """

        prompts_it = DataService.iter_prompt(data_dict_it=data_dict_it, prompt=prompt, parse_fields_func=iter_params)

        for batch in BatchIterator(prompts_it, batch_size=batch_size):
            index, input = zip(*batch)
            ctx = BatchingPipelineLauncher.run(
                pipeline=self.pipeline,
                pipeline_ctx=PipelineContext(d={"index": index, "input": input}),
                src_key="input")

            # Target.
            d = ctx._d

            for batch_ind in range(len(d["input"])):
                yield {k: v[batch_ind] for k, v in d.items()}

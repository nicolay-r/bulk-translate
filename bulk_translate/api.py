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
                do_translate_entity=translate_spans,
                is_span_func=lambda term: isinstance(term, Span)),
            MapPipelineItem(map_func=lambda term:
                ([term.DisplayValue] + ([term.content] if term.content is not None else []))
                if isinstance(term, Span) else term),
            BasePipelineItem(src_func=lambda src: list(src))
        ]

    def handle_batch(self, batch, col_output, col_prompt=None):
        assert(isinstance(batch, list))

        if col_prompt is None:
            col_prompt = col_output

        ctx = BatchingPipelineLauncher.run(pipeline=self.pipeline,
                                           pipeline_ctx=PipelineContext(d={col_prompt: batch}),
                                           src_key=col_prompt)

        # Target.
        d = ctx._d

        for batch_ind in range(len(d[col_prompt])):

            yield {(k if k != BasePipelineItem.DEFAULT_RESULT_KEY else col_output):
                       v[batch_ind] for k, v in d.items()}

    def iter_translated_data(self, data_dict_it, schema, batch_size=1, keep_prompt=False):
        """ This is the main API method for calling.
        """
        assert(isinstance(schema, dict))

        for data_batch in BatchIterator(data_dict_it, batch_size=batch_size):
            for col_output, prompt in schema.items():

                prompts_it = DataService.iter_prompt(data_dict_it=data_batch,
                                                     prompt=prompt,
                                                     parse_fields_func=iter_params)

                handled_data_it = self.handle_batch(batch=list(prompts_it),
                                                    col_output=col_output,
                                                    col_prompt=f"prompt_{col_output}" if keep_prompt else None)

                # Applying updated content from the handled column.
                for record_ind, record in enumerate(handled_data_it):
                    data_batch[record_ind] |= record

            for item in data_batch:
                yield item

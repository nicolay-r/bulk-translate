from bulk_translate.src.pipeline.items.base import BasePipelineItem
from bulk_translate.src.span import Span


class TextSpansParser(BasePipelineItem):

    def __init__(self, **kwargs):
        super(TextSpansParser, self).__init__(**kwargs)

    def apply_core(self, input_data, pipeline_ctx):
        assert(isinstance(input_data, list))
        content = [Span(value=w[0], content=w[1] if len(w) > 1 else None)
                   if isinstance(w, list) else w for w in input_data]
        return content

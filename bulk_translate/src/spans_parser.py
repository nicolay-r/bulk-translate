from arekit.common.entities.base import Entity
from arekit.common.pipeline.items.base import BasePipelineItem


class TextSpansParser(BasePipelineItem):

    def __init__(self, **kwargs):
        super(TextSpansParser, self).__init__(**kwargs)

    def apply_core(self, input_data, pipeline_ctx):
        assert(isinstance(input_data, list))
        content = [Entity(value=w[0], e_type=w[1] if len(w) > 1 else None)
                   if isinstance(w, list) else w for w in input_data]
        return content

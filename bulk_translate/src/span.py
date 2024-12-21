class Span(object):

    def __init__(self, value, content=None, display_value=None):
        assert(isinstance(value, str) and len(value) > 0)
        assert(isinstance(display_value, str) or display_value is None)
        self.__value = value
        self.__display_value = display_value
        self.content = content

    @property
    def Value(self):
        return self.__value

    @property
    def DisplayValue(self):
        return self.__value if self.__display_value is None else self.__display_value

    def set_display_value(self, caption):
        assert(isinstance(caption, str))
        self.__display_value = caption
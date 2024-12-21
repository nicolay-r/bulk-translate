import logging
import sys


def iter_params(text, keep_strings=True):
    assert(isinstance(text, str))
    beg = 0
    while beg < len(text):
        try:
            pb = text.index('{', beg)
        except ValueError:
            break
        pe = text.index('}', beg+1)

        # Yield prefix.
        if beg < pb and keep_strings:
            yield [text[beg:pb]]

        # Yield argument.
        yield text[pb+1:pe]
        beg = pe+1

    # Yield suffix.
    if beg < len(text) and keep_strings:
        yield [text[beg:len(text)]]


def parse_filepath(filepath, default_filepath=None, default_ext=None):
    """ This is an auxiliary function for handling sources and targets from cmd string.
    """
    if filepath is None:
        return default_filepath, default_ext, None
    info = filepath.split(":")
    filepath = info[0]
    meta = info[1] if len(info) > 1 else None
    ext = filepath.split('.')[-1] if default_ext is None else default_ext
    return filepath, ext, meta


def test_translate_demo(iter_answers=None):

    while True:

        user_input = input(f"Enter your text "
                           f"(or 'exit' to quit): ")

        if user_input.lower() == 'exit':
            break

        lang_from = input("From language (or Enter for `auto`): ")

        if lang_from == "":
            lang_from = None

        lang_to = input("To language: ")

        # Finally asking LLM.
        for a in iter_answers(user_input, lang_from, lang_to):
            print(a)


def setup_custom_logger(name, add_screen_handler=False, filepath=None):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if add_screen_handler:
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger.addHandler(screen_handler)

    if filepath is not None:
        handler = logging.FileHandler(filepath, mode='w')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
import argparse
import os
import sys

from tqdm import tqdm

from source_iter.service_csv import CsvService
from source_iter.service_jsonl import JsonlService

from bulk_translate.api import Translator
from bulk_translate.src.service_args import CmdArgsService
from bulk_translate.src.service_dynamic import dynamic_init
from bulk_translate.src.utils import test_translate_demo, setup_custom_logger, parse_filepath


CWD = os.getcwd()


if __name__ == '__main__':
    
    logger = setup_custom_logger("bulk-ner")

    parser = argparse.ArgumentParser(description="Apply Translator")

    parser.add_argument('--adapter', dest='adapter', type=str, default=None)
    parser.add_argument('--batch-size', dest='batch_size', type=int, default=1)
    parser.add_argument('--prompt', dest='prompt', type=str, default="{text}")
    parser.add_argument('--src', dest='src', type=str, default=None)
    parser.add_argument('--output', dest='output', type=str, default=None)
    parser.add_argument('--parse-entities', action='store_true', default=False)
    parser.add_argument('--translate-entity', action='store_true', default=False)
    parser.add_argument('--chunk-limit', dest='chunk_limit', type=int, default=128)

    native_args, model_args = CmdArgsService.partition_list(lst=sys.argv, sep="%%")
    custom_args_dict = CmdArgsService.args_to_dict(model_args)

    args = parser.parse_args(args=native_args[1:])

    # Provide the default output.
    if args.output is None and args.src is not None:
        args.output = ".".join(args.src.split('.')[:-1]) + "-converted.jsonl"

    input_formatters = {
        None: lambda _: test_translate_demo(
            iter_answers=lambda example, lang_from, lang_to:
                translator.iter_translated_data(data_dict_it=iter([(0, example)]),
                                                prompt=args.prompt,
                                                batch_size=args.batch_size)),
        "csv": lambda filepath: CsvService.read(src=filepath, as_dict=True, skip_header=True,
                                                delimiter=custom_args_dict.get("delimiter", ","),
                                                escapechar=custom_args_dict.get("escapechar", None)),
        "tsv": lambda filepath: CsvService.read(src=filepath, as_dict=True, skip_header=True,
                                                delimiter=custom_args_dict.get("delimiter", "\t"),
                                                escapechar=custom_args_dict.get("escapechar", None)),
        "jsonl": lambda filepath: JsonlService.read(src=filepath)
    }

    output_formatters = {
        "jsonl": lambda dicts_it: JsonlService.write(target=args.output, data_it=dicts_it)
    }

    models_preset = {
        "dynamic": lambda: dynamic_init(src_dir=CWD, class_filepath=ner_model_name, class_name=ner_model_params)(
            # The rest of parameters could be provided from cmd.
            **custom_args_dict)
    }

    # Parse the model name.
    params = args.adapter.split(':')

    # Making sure that we refer to the supported preset.
    assert (params[0] in models_preset)

    # Completing the remaining parameters.
    ner_model_name = params[1] if len(params) > 1 else params[-1]
    ner_model_params = ':'.join(params[2:]) if len(params) > 2 else None

    translator = Translator(parse_spans=args.parse_entities,
                            translate_spans=args.translate_entity,
                            translation_model=models_preset["dynamic"](),
                            **custom_args_dict)

    translation_model = models_preset["dynamic"]()

    _, src_ext, _ = parse_filepath(args.src)
    texts_it = input_formatters[src_ext](args.src)

    # There is no need to perform export.
    if src_ext is None:
        exit(0)

    ctxs_it = translator.iter_translated_data(data_dict_it=texts_it, prompt=args.prompt, batch_size=args.batch_size)
    output_formatters["jsonl"](dicts_it=tqdm(ctxs_it, desc=f"Processing `{args.src}`"))

    logger.info(f"Saved: {args.output}")

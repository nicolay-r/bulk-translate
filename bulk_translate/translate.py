import argparse
import json
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
    parser.add_argument('--prompt', dest='prompt', type=str, default=None)
    parser.add_argument('--keep-prompt', action='store_true', default=False)
    parser.add_argument('--default-field-output', dest='default_field_output', default="output")
    parser.add_argument('--schema', dest='schema', type=str, default=None)
    parser.add_argument('--src', dest='src', type=str, default=None)
    parser.add_argument('--output', dest='output', type=str, default=None)
    parser.add_argument('--translate-entity', action='store_true', default=False)
    parser.add_argument('--chunk-limit', dest='chunk_limit', type=int, default=128)

    # Extract native arguments.
    native_args = CmdArgsService.extract_native_args(sys.argv, end_prefix="%%")
    args = parser.parse_args(args=native_args[1:])
    
    # Reading the prompting schema.
    if args.prompt is not None and args.schema is not None:
        raise Exception("Error: you can't set both schema and prompt!")
    if args.prompt is not None:
        schema = {args.default_field_output: args.prompt}
    else:
        schema = json.loads(args.schema)

    # Extract csv-related arguments.
    csv_args = CmdArgsService.find_grouped_args(lst=sys.argv, starts_with="%%csv", end_prefix="%%")
    csv_args_dict = CmdArgsService.args_to_dict(csv_args)

    # Extract model-related arguments and Initialize Large Language Model.
    model_args = CmdArgsService.find_grouped_args(lst=sys.argv, starts_with="%%m", end_prefix="%%")
    model_args_dict = CmdArgsService.args_to_dict(model_args)

    # Provide the default output.
    if args.output is None and args.src is not None:
        args.output = ".".join(args.src.split('.')[:-1]) + "-converted.jsonl"

    input_formatters = {
        None: lambda _: test_translate_demo(
            iter_answers=lambda example, lang_from, lang_to:
                translator.iter_translated_data(data_dict_it=iter([(0, example)]),
                                                schema=schema,
                                                keep_prompt=args.keep_prompt,
                                                batch_size=args.batch_size)),
        "csv": lambda filepath: CsvService.read(src=filepath, as_dict=True, skip_header=True,
                                                delimiter=csv_args_dict.get("delimiter", ","),
                                                escapechar=csv_args_dict.get("escapechar", None)),
        "tsv": lambda filepath: CsvService.read(src=filepath, as_dict=True, skip_header=True,
                                                delimiter=csv_args_dict.get("delimiter", "\t"),
                                                escapechar=csv_args_dict.get("escapechar", None)),
        "jsonl": lambda filepath: JsonlService.read(src=filepath)
    }

    output_formatters = {
        "jsonl": lambda dicts_it: JsonlService.write(target=args.output, data_it=dicts_it)
    }

    models_preset = {
        "dynamic": lambda: dynamic_init(src_dir=CWD, class_filepath=ner_model_name, class_name=ner_model_params)(
            # The rest of parameters could be provided from cmd.
            **model_args_dict)
    }

    # Parse the model name.
    params = args.adapter.split(':')

    # Making sure that we refer to the supported preset.
    assert (params[0] in models_preset)

    # Completing the remaining parameters.
    ner_model_name = params[1] if len(params) > 1 else params[-1]
    ner_model_params = ':'.join(params[2:]) if len(params) > 2 else None

    translator = Translator(translate_spans=args.translate_entity,
                            translation_model=models_preset["dynamic"](),
                            **model_args_dict)

    translation_model = models_preset["dynamic"]()

    _, src_ext, _ = parse_filepath(args.src)
    texts_it = input_formatters[src_ext](args.src)

    # There is no need to perform export.
    if src_ext is None:
        exit(0)

    ctxs_it = translator.iter_translated_data(data_dict_it=texts_it, schema=schema, batch_size=args.batch_size)
    output_formatters["jsonl"](dicts_it=tqdm(ctxs_it, desc=f"Processing `{args.src}`"))

    logger.info(f"Saved: {args.output}")

# bulk-translate 0.24.1
A tiny Python no-string package for performing translation of a massive `CSV`/`JSONL` files

**TODO:**
- [x] Unit-test
- [ ] Add and describe feature of **already annotated entities** in text (AREkit API citation) (Issue #1)
    https://github.com/nicolay-r/bulk-translate/issues/1
- [ ] Describe features of the Translator PipelineItem implementation: `fast-mode` and `accurate`

## Installation

```bash
pip install git+https://github.com/nicolay-r/bulk-translate
```

## Usage

```bash
python -m bulk_translate.translate \
    --src "test/data/test.tsv" \
    --prompt "{text}" \
    --adapter "dynamic:models/googletrans_310a.py:GoogleTranslateModel" \
    --output "test-translated.jsonl" \
    %% \
    --src "auto" \
    --dest "ru"
```

## Powered by

* AREkit [[github]](https://github.com/nicolay-r/AREkit)

<p float="left">
<a href="https://github.com/nicolay-r/AREkit"><img src="https://github.com/nicolay-r/ARElight/assets/14871187/01232f7a-970f-416c-b7a4-1cda48506afe"/></a>
</p>

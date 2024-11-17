# bulk-translate 0.24.1
![](https://img.shields.io/badge/Python-3.9-brightgreen.svg)
![](https://img.shields.io/badge/AREkit-0.25.0-orange.svg)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nicolay-r/bulk-translate/blob/master/bulk_translate_demo.ipynb)


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

> **NOTE:** If you wish to translate parse entities, you can use `parse-entities` flag

For the following [`test.tsv` example data](/test/data/test.tsv) with annotated entities enclosed in square brackets:

```bash
python -m bulk_translate.translate \
    --src "test/data/test.tsv" \
    --prompt "{text}" \
    --adapter "dynamic:models/googletrans_310a.py:GoogleTranslateModel" \
    --output "test-translated.jsonl" \
    --parse-entities \
    %% \
    --src "auto" \
    --dest "ru"
```


## Powered by

* AREkit [[github]](https://github.com/nicolay-r/AREkit)

<p float="left">
<a href="https://github.com/nicolay-r/AREkit"><img src="https://github.com/nicolay-r/ARElight/assets/14871187/01232f7a-970f-416c-b7a4-1cda48506afe"/></a>
</p>

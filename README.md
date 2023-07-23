**nbdocgen** is a command line tool to generate documentation for each and every cell in a Jupyter notebook using OpenAI.

# Getting Started

## Prerequisites
- Python >=3.8
- [Poetry](https://python-poetry.org/)
- OpenAI API Key

## Installation
```
git clone https://github.com/santiadavani/nbdocgen
cd nbdocgen
poetry shell
poetry install
pip install .
```

## Usage
Set OPENAI_API_KEY environment variable. If you don't have a key please check documentation [here](https://platform.openai.com/docs/api-reference/authentication)

`export OPENAI_API_KEY=<OPENAI_API_KEY>`

You can check all the options using `--help`.
```
(nbdocgen-py3.9) bash-3.2$ nbdocgen --help
Usage: nbdocgen [OPTIONS]

Options:
  --input PATH          Input Jupyter Notebook
  --output PATH         Output Jupyter Notebook
  --temperature FLOAT   Temperate for OpenAI  [default: 0.7]
  --top_p FLOAT         Top p for OpenAI  [default: 1.0]
  --max_tokens INTEGER  Max tokens for OpenAI completion  [default: 256]
  --base_prompt TEXT    Base prompt for OpenAI completion  [default: Please
                        generate a two sentence markdown documentation for the
                        given Python code.]
  --help                Show this message and exit.
```

## Example
In this example, we show how to use `temperature` and `base_prompt` options. 

```
nbdocgen --input ~/Downloads/input_notebook.ipynb \
--output ./output_notebook.ipynb --temperature 0.3 \
--base_prompt "Please generate 5 sentence markdown documentation for the code below"
```

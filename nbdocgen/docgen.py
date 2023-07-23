import json
import click
from rich import print
from uuid import uuid4
from rich.progress import track
from time import sleep
import logging
from rich.logging import RichHandler
import openai
import os
import sys

FORMAT = "%(message)s"
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "ERROR"),
    format="%(asctime)s - %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


def generate_markdown(documentation=["# Test cell"]):
    markdown_template = {}
    markdown_template["cell_type"] = "markdown"
    markdown_template["metadata"] = {"id": str(uuid4())[:12]}
    markdown_template["source"] = documentation
    return markdown_template


def generate_documentation(
    prompt, openai_api_key, temperature=0.7, max_tokens=256, top_p=1.0
):
    openai.api_key = openai_api_key

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["message"]["content"]


@click.command()
@click.option(
    "--input",
    help="Input Jupyter Notebook",
    type=click.Path(),
)
@click.option("--output", help="Output Jupyter Notebook", type=click.Path())
@click.option(
    "--temperature",
    help="Temperate for OpenAI",
    default=0.7,
    type=float,
    show_default=True,
)
@click.option(
    "--top_p",
    help="Top p for OpenAI",
    default=1.0,
    type=float,
    show_default=True,
)
@click.option(
    "--max_tokens",
    help="Max tokens for OpenAI completion",
    default=256,
    type=int,
    show_default=True,
)
@click.option(
    "--base_prompt",
    help="Base prompt for OpenAI completion",
    default="Please generate a two sentence markdown documentation for the given Python code.",
    type=str,
    show_default=True,
)
def docgen(**kwargs) -> int:
    input_file = kwargs["input"]
    output_file = kwargs["output"]
    temperature = kwargs["temperature"]
    top_p = kwargs["top_p"]
    max_tokens = kwargs["max_tokens"]
    base_prompt = kwargs["base_prompt"]

    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if not openai_api_key:
        log.error("OPENAI API KEY is not set")
        return -1

    if not os.path.exists(input_file):
        log.error("%s does not exist" % input_file)
        return -1

    if not output_file:
        log.error("output file path is empty")
        return -1

    if input_file == output_file:
        log.error(
            "%s\nInput and output file names are the same - please use a different filename for output notebook"
            % (output_file)
        )
        return -1

    if os.path.exists(output_file):
        log.error("%s already exists - please use a different name" % output_file)
        return -1

    with open(input_file, "r") as fp:
        data = json.load(fp)

    output_data = data
    cells = output_data.pop("cells")

    prompt_template = """
    {base_prompt}
    ```python
    {code}
    ```
    """

    output_cells = []
    for cell in track(cells):
        if cell["cell_type"] == "code":
            code = "\n".join(cell["source"])
            prompt = prompt_template.format(base_prompt=base_prompt,code=code)
            documentation = generate_documentation(
                prompt=prompt,
                openai_api_key=openai_api_key,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )
            markdown = generate_markdown(documentation=documentation)
            output_cells.append(markdown)
            sleep(1)
        output_cells.append(cell)

    output_data["cells"] = output_cells

    with open(output_file, "w") as fp:
        json.dump(output_data, fp)

    return 0


if __name__ == "__main__":
    sys.exit(docgen())  # pragma: no cover

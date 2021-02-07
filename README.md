<div align="center">

<h1>Crusher</h1>

<strong>>> <i>Crush a deeply nested JSON string</i> <<</strong>

<h3></h3>


<br></br>
![Codecov](https://img.shields.io/codecov/c/github/rednafi/crusher?color=pink&style=flat-square&logo=appveyor)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square&logo=appveyor)](https://github.com/python/black)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square&logo=appveyor)](./LICENSE)
<br></br>

</div>

## Description

**Crusher** lets you flatten a deeply nested JSON file or string, and export it to markdown through a simple CLI. It also prints out the flattened JSON with type annotated variables for inspection.

I primarily wrote it to automate the tedious part of documenting REST API endpoints in Postman.

## Installation

Install it via Pip:

```
pip install crusher
```

## Usage

* Inspect the help message:

```
crusher --help
```

```
usage: crusher [-h] [--json JSON] [--json_path JSON_PATH] [--prefix PREFIX]
               [--delimiter DELIMITER] [--hide_values] [--export_path EXPORT_PATH] [--demo]

🗿 Crusher: Flatten a JSON String / File.

optional arguments:
  -h, --help            show this help message and exit
  --json JSON           provide the target json string
  --json_path JSON_PATH
                        provide the target json file path
  --prefix PREFIX       append a prefix before path
  --delimiter DELIMITER
                        provide preferred delimiter
  --hide_values         show or hide attribute values
  --export_path EXPORT_PATH
                        export result to `.md` file
  --demo                show the output of an example json
```

* Flatten a JSON string. You can directly provide your JSON string to the CLI and it will flatten it and dump it on the stdout. To do so—

```bash
crusher \
--json='{"person": {"first_name": "Warner", "last_name": "Hysenberg", "age": 30}}'
```

```
                                        🍺 Crushed JSON 🍺

 🌳  person.first_name : str  =>  Warner
 🌳  person.last_name : str  =>  Hysenberg
 🌳  person.age : int  =>  30
```

* Additionally, you may choose to export the output as a markdown file. To do so, you'll have to provide the export part of the destination file—

```
crusher \
--json='{"person": {"first_name": "Warner", "last_name": "Hysenberg", "age": 30}}' \
--export_path=result.md
```

If you inspect the content of the `result.md` file, you'll see something like this:

```
* `person.first_name`: `str` => `Warner`

* `person.last_name`: `str` => `Hysenberg`

* `person.age`: `int` => `30`
```


* Directly providing a long string of deeply nested JSON string can be cumbersome. To avoid that—you can proide a `.json` file directly. To do so—

```
crusher --json_path=examples/example.json --export_path=examples/result.md
```

This should give you similary output as before.

* Also, you may want to exclude the result of an JSON attribute—useful while doing documentation. To do so, use the `--hide_values` flag.

```
crusher \
--json='{"person": {"first_name": "Warner", "last_name": "Hysenberg", "age": 30}}' \
--export_path=result.md \
--hide_values
```

```
                                        🍺 Crushed JSON 🍺

 🌳  person.first_name : str
 🌳  person.last_name : str
 🌳  person.age : int
```


<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>

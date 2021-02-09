import argparse
import json
import sys

from rich.console import Console
from rich.emoji import Emoji
from rich.traceback import install

install()

_DEMO_STR = """


{
    "uuid": "3934de86-e308-4407-b411-e57b23b9f1e5",
    "alternate_id": "123123",
    "account": "AnyTestNow",
    "provider": {
        "user": {
            "first_name": "Lisa",
            "last_name": "Leslie",
            "email": "leslie@clinic.com"
        },
        "uuid": "432b3eda-909c-4500-b5bd-9de2819ab1c1",
        "npi": "5555555555"
    },
    "patient": {
        "uuid": "b2ccecc7-58b9-4836-b64d-5372bcf82788",
        "id": "5",
        "alternate_id": "",
        "user": {
            "first_name": "Dell",
            "last_name": "Curry",
            "email": "dcurry@mailinator.com"
        },
        "middle_initial": "D",
        "gender": "M",
        "birth_date": "1980-01-05",
        "suffix": "",
        "address1": "23 jump st",
        "address2": "suite 3",
        "city": "12city",
        "state": "",
        "country": "Armenia",
        "zip_code": "123423",
        "social_security": "555-55-5555",
        "phone_number": "(744) 555-4342",
        "drivers_license": "",
        "ethnicity": "U",
        "race": "U",
        "reference_integration": null,
        "bill_to": "Insurance",
        "accounts": [
            "f16693a2-c70a-4056-bbc1-e48dda71474a",
            "3c49f9db-b900-43a8-a5e1-47dbec8f7fd0",
            "e1e9a0d1-52ba-4904-bbdc-eaaebf05733b"
        ],
        "providers": [
            "a962ed42-c824-499d-bedf-f0da7efed3fe",
            "432b3eda-909c-4500-b5bd-9de2819ab1c1",
            "a47ba996-2095-497c-8870-787a70faa6e6"
        ]
    },
    "code": "2021-0000071",
    "status": "Unreceived",
    "accession_number": null,
    "is_acknowledged_by_external_user": false,
    "in_house_lab_locations": [],
    "bill_to": "Insurance",
    "test_panels": [
        {
            "uuid": "51f5f9c6-fb43-4ae1-804a-c8c2fc541de6",
            "test_panel_type": {
                "uuid": "60a30ac0-a6b3-4774-9686-39e0f37cbdba",
                "alternate_id": "",
                "name": "Anticonvulsants"
            },
            "samples": [
                {
                    "uuid": "ad543d1c-bf7e-4ada-a628-19d737d84edb",
                    "code": "2021-0000071-U-1",
                    "alternate_id": "",
                    "collection_date": null,
                    "barcode": "20210000071U1",
                    "clia_sample_type": {
                        "uuid": "18fc0c28-5e89-4855-9ea2-568590737aa4",
                        "name": "Urine"
                    },
                    "collection_temperature": "",
                    "comments": ["00"]
                }
            ]
        }
    ],
    "origin_entity": "Dendi API",
    "submitted_date": "2021-01-20T14:17:41.122094",
    "reference_lab_received_date": null,
    "origin": "Reference Lab",
    "icd10_codes": [
        {
            "uuid": "b473220f-2abc-45f5-8355-9374c263627f",
            "full_code": "A00.0"
        }
    ],
    "reference_id": "2020-0021920",
    "reference_integration": null,
    "notes_by_provider": "Testing an API call.",
    "bulk_order_uuid": null
}
"""


class ArgCombinationError(Exception):
    """Raised when an invalid argument combination is provided."""


def flatten(dct, prefix="", delimiter="."):
    """Turn a nested dictionary into a flattened dictionary

    Parameters
    ----------
    dct : dict
        The dictionary to flatten
    prefix : bool, optional
        The string to prepend to dictionary's keys, by default False
    delimiter : str, optional
        str, by default "."

    Returns
    -------
    dict
        Flattened dictionary

    Examples
    --------

    """

    paths = []
    for k, v in dct.items():
        new_k = str(prefix) + delimiter + k if prefix else k

        if isinstance(v, dict):
            paths.extend(flatten(v, new_k, delimiter).items())

        elif isinstance(v, list):
            for k, v in enumerate(v):
                paths.extend(flatten({str(k): v}, new_k, delimiter).items())

        else:
            paths.append((new_k, v))

    return dict(paths)


class Color:
    @staticmethod
    def key(text):
        return f"[yellow]{text}[/yellow]"

    @staticmethod
    def type(text):
        return f"[magenta]{text}[/magenta]"

    @staticmethod
    def arrow(text):
        return f"[green]{text}[/green]"

    @staticmethod
    def value(text):
        return f"[cyan]{text}[/cyan]"


class Crusher:
    def __init__(
        self,
        dct,
        prefix="",
        delimiter=".",
        show_value=True,
        export_path=None,
        _flatten=flatten,
        _console=Console,
        _emoji=Emoji,
        _color=Color,
    ):
        self.dct = dct
        self.prefix = prefix
        self.delimiter = delimiter
        self.show_value = show_value
        self.export_path = export_path
        self._flatten = _flatten
        self._console = _console()
        self._emoji = _emoji
        self._color = _color()

    @property
    def flat_dct(self):
        return self._flatten(self.dct, prefix=self.prefix, delimiter=self.delimiter)

    def print_json(self):
        """Print a flattened JSON string."""

        emo = self._emoji("beer")

        self._console.print(
            f"\n{emo} Crushed JSON {emo}",
            end="\n\n",
            style="bold",
            justify="center",
        )

        emo = self._emoji("deciduous_tree")
        color = self._color

        for k, v in self.flat_dct.items():
            if self.show_value:
                self._console.print(
                    f" {emo} ",
                    color.key(k),
                    ":",
                    color.type(type(v).__name__),
                    color.arrow(" => "),
                    color.value(v),
                )
            else:
                self._console.print(
                    f" {emo} ",
                    color.key(k),
                    ":",
                    color.type(type(v).__name__),
                )

    def export_markdown(self):
        """Export to markdown."""

        rows = []
        for k, v in self.flat_dct.items():
            if self.show_value:
                row = f"* `{k}`: `{type(v).__name__}` => `{v}`"
            else:
                row = f"* `{k}`: `{type(v).__name__}`"
            rows.append(row)

        with open(self.export_path, "+w") as f:
            f.write("\n\n".join(rows))

    def crush(self):
        self.print_json()

        if self.export_path:
            self.export_markdown()


class CLI:
    def __init__(self, _crusher=Crusher, _help_on_missing_arg=True):
        self._crusher = _crusher
        self._help_on_missing_arg = _help_on_missing_arg

    @staticmethod
    def load_json(json_str, json_path=None, demo=False, _demo_str=_DEMO_STR):
        if demo:
            return json.loads(_demo_str)

        if json_str:
            return json.loads(json_str)

        with open(json_path) as f:
            return json.load(f)

    def handle_errors(self, parser, args):
        if self._help_on_missing_arg:
            try:
                sys.argv[1]
            except IndexError:
                parser.print_help()
                parser.exit()

        if args.json and args.json_path:
            raise ArgCombinationError("This combination of arguments is not allowed.")

        elif args.demo and any((args.json, args.json_path)):
            raise ArgCombinationError("This combination of arguments is not allowed.")

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(
            description="🗿 Crusher: Flatten a JSON String / File.",
        )
        parser.add_argument(
            "--json",
            help="provide the target json string",
        )
        parser.add_argument(
            "--json_path",
            help="provide the target json file path",
        )
        parser.add_argument(
            "--prefix",
            default="",
            help="append a prefix before path",
        )
        parser.add_argument(
            "--delimiter",
            default=".",
            help="provide preferred delimiter",
        )
        parser.add_argument(
            "--hide_values",
            action="store_false",
            help="show or hide attribute values",
        )
        parser.add_argument(
            "--export_path",
            help="export result to `.md` file",
        )
        parser.add_argument(
            "--demo",
            action="store_true",
            help="show the output of an example json",
        )

        return parser

    def entrypoint(self, argv=None):
        parser = self.get_parser()
        args = parser.parse_args(argv)

        # Handling errors.
        self.handle_errors(parser, args)

        dct = self.load_json(args.json, args.json_path, args.demo)
        sp = self._crusher(
            dct,
            prefix=args.prefix,
            delimiter=args.delimiter,
            show_value=args.hide_values,
            export_path=args.export_path,
        )

        sp.crush()


def cli_entrypoint(argv=None, _help_on_missing_arg=True):
    cli = CLI(_help_on_missing_arg=_help_on_missing_arg)
    cli.entrypoint(argv=argv)


# if __name__ == '__main__':
#     cli_entrypoint(argv=['--json={}'],_help_on_missing_arg=False)

import pytest

from crusher import ArgCombinationError, Color, flatten, Crusher, Console, Emoji


def test_color():
    color = Color()

    assert color.key("Hello") == "[yellow]Hello[/yellow]"
    assert color.type("str") == "[magenta]str[/magenta]"
    assert color.arrow("=>") == "[green]=>[/green]"
    assert color.value("uuid") == "[cyan]uuid[/cyan]"


def test_arg_combination_arror(capsys):

    print(ArgCombinationError("Argument combination not allowed."))
    capture = capsys.readouterr()

    assert "Argument combination" in capture.out
    assert capture.err == ""

    with pytest.raises(ArgCombinationError):
        raise ArgCombinationError()


def test_flatten_v0():
    d = {
        "i": {
            "j": {
                "k": [],
            }
        }
    }

    r = flatten(d, prefix="", delimiter=".")
    assert r == {}


def test_flatten_v1():
    d = {
        "i": {
            "j": {
                "k": ["dd", "ee"],
            }
        }
    }
    r = flatten(d, prefix="", delimiter=".")
    assert r == {
        "i.j.k.0": "dd",
        "i.j.k.1": "ee",
    }


def test_flatten_v2():
    d = {
        "_id": "601ef24ab93aad141d0a74e0",
        "index": 0,
        "guid": "36b91e8e-df9d-4d9f-bc67-54eee11cd07a",
        "isActive": False,
        "balance": "$3,490.51",
        "picture": "http://placehold.it/32x32",
        "age": 30,
        "eyeColor": "green",
        "name": "Katrina Sharpe",
        "gender": "female",
        "company": "ZILODYNE",
        "email": "katrinasharpe@zilodyne.com",
        "phone": "+1 (879) 400-2550",
        "address": "618 Vermont Street, Moquino, Guam, 6536",
        "about": "Sit aliqua voluptate do duis officia. Quis esse fugiat incididunt aliqua officia id tempor veniam ex esse duis excepteur excepteur sit. Ex Lorem mollit incididunt dolore dolore. Quis commodo cupidatat irure laborum aliqua labore elit. Velit non ullamco ut mollit mollit ex fugiat officia incididunt. Ullamco sunt sunt adipisicing minim velit in aliquip est ipsum commodo sint pariatur officia ullamco. Ipsum aliquip labore esse minim pariatur.\r\n",
        "registered": "2020-08-29T03:27:41 -06:00",
        "latitude": 45.909483,
        "longitude": -130.807383,
        "tags.0": "reprehenderit",
        "tags.1": "adipisicing",
        "tags.2": "do",
        "tags.3": "laboris",
        "tags.4": "commodo",
        "tags.5": "magna",
        "tags.6": "enim",
        "friends.0.id": 0,
        "friends.0.name": "Britney Guthrie",
        "friends.1.id": 1,
        "friends.1.name": "Polly Chen",
        "friends.2.id": 2,
        "friends.2.name": "Jane Ross",
        "greeting": "Hello, Katrina Sharpe! You have 10 unread messages.",
        "favoriteFruit": "banana",
    }
    expected_r = {
        "_id": "601ef24ab93aad141d0a74e0",
        "index": 0,
        "guid": "36b91e8e-df9d-4d9f-bc67-54eee11cd07a",
        "isActive": False,
        "balance": "$3,490.51",
        "picture": "http://placehold.it/32x32",
        "age": 30,
        "eyeColor": "green",
        "name": "Katrina Sharpe",
        "gender": "female",
        "company": "ZILODYNE",
        "email": "katrinasharpe@zilodyne.com",
        "phone": "+1 (879) 400-2550",
        "address": "618 Vermont Street, Moquino, Guam, 6536",
        "about": "Sit aliqua voluptate do duis officia. Quis esse fugiat incididunt aliqua officia id tempor veniam ex esse duis excepteur excepteur sit. Ex Lorem mollit incididunt dolore dolore. Quis commodo cupidatat irure laborum aliqua labore elit. Velit non ullamco ut mollit mollit ex fugiat officia incididunt. Ullamco sunt sunt adipisicing minim velit in aliquip est ipsum commodo sint pariatur officia ullamco. Ipsum aliquip labore esse minim pariatur.\r\n",
        "registered": "2020-08-29T03:27:41 -06:00",
        "latitude": 45.909483,
        "longitude": -130.807383,
        "tags.0": "reprehenderit",
        "tags.1": "adipisicing",
        "tags.2": "do",
        "tags.3": "laboris",
        "tags.4": "commodo",
        "tags.5": "magna",
        "tags.6": "enim",
        "friends.0.id": 0,
        "friends.0.name": "Britney Guthrie",
        "friends.1.id": 1,
        "friends.1.name": "Polly Chen",
        "friends.2.id": 2,
        "friends.2.name": "Jane Ross",
        "greeting": "Hello, Katrina Sharpe! You have 10 unread messages.",
        "favoriteFruit": "banana",
    }

    assert flatten(d, prefix="", delimiter=".") == expected_r


def test_flatten_prefix():
    d = {
        "i": {
            "j": {
                "k": ["dd", "ee"],
            }
        }
    }

    expected_r = {
        "||.i.j.k.0": "dd",
        "||.i.j.k.1": "ee",
    }

    assert flatten(d, prefix="||", delimiter=".") == expected_r


def test_flatten_delimiter():
    d = {
        "i": {
            "j": {
                "k": ["dd", "ee"],
            }
        }
    }

    expected_r = {
        "i$$j$$k$$0": "dd",
        "i$$j$$k$$1": "ee",
    }

    assert flatten(d, prefix="", delimiter="$$") == expected_r


def test_crusher_init():
    d = {
        "i": {
            "j": {
                "k": ["dd", "ee"],
            }
        }
    }

    # Initializing with the default parameter.
    cr = Crusher(dct=d)

    # Checking whether the dict was passed correctly.
    assert cr.dct == d

    # Checking the default parameters.
    assert cr.prefix == ""
    assert cr.delimiter == "."
    assert cr.show_value is True
    assert cr.export_path is None

    # Checking that the injected classes are passed and initialized properly.
    assert isinstance(cr._color, Color)
    assert isinstance(cr._console, Console)
    assert cr._emoji is Emoji


def test_crusher_flat_dct():
    d = {
        "i": {
            "j": {
                "k": ["dd", "ee"],
            }
        }
    }

    cr = Crusher(dct=d)
    assert cr.flat_dct == {"i.j.k.0": "dd", "i.j.k.1": "ee"}


def test_crusher_print_json(capsys):
    d = {
        "i": {
            "j": {
                "k": ["dd", "ee"],
            }
        }
    }

    cr = Crusher(dct=d)
    cr.print_json()

    out, err = capsys.readouterr()

    assert err == ""
    assert "🍺 Crushed JSON 🍺" in out
    assert "🌳  i.j.k.0 : str  =>  dd" in out
    assert "🌳  i.j.k.1 : str  =>  ee" in out


def test_crusher_export_markdown(tmpdir):
    d = {
        "i": {
            "j": {
                "k": ["dd", "ee"],
            }
        }
    }

    file = tmpdir.join("output.md")
    cr = Crusher(dct=d, export_path=file.strpath)
    cr.export_markdown()

    assert "* `i.j.k.0`: `str` => `dd`" in file.read()
    assert "* `i.j.k.1`: `str` => `ee`" in file.read()


def test_crusher_crush(capsys, tmpdir):
    d = {
        "i": {
            "j": {
                "k": ["dd", "ee"],
            }
        }
    }

    file = tmpdir.join("output.md")
    cr = Crusher(dct=d, export_path=file.strpath)
    cr.crush()

    out, err = capsys.readouterr()

    assert err == ""
    assert "🍺 Crushed JSON 🍺" in out
    assert "🌳  i.j.k.0 : str  =>  dd" in out
    assert "🌳  i.j.k.1 : str  =>  ee" in out

    assert "* `i.j.k.0`: `str` => `dd`" in file.read()
    assert "* `i.j.k.1`: `str` => `ee`" in file.read()

    # Testing other combinations of input parameters.
    cr = Crusher(
        dct=d,
        export_path=file.strpath,
        prefix="@",
        delimiter="|",
        show_value=False,
    )
    cr.crush()

    out, err = capsys.readouterr()

    assert err == ""
    assert "🍺 Crushed JSON 🍺" in out
    assert "🌳  @|i|j|k|0 : str" in out
    assert "🌳  @|i|j|k|1 : str" in out

    assert "* `@|i|j|k|0`: `str`" in file.read()
    assert "* `@|i|j|k|1`: `str`" in file.read()

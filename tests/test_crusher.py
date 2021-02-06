from crusher import Color


def test_color():
    color = Color()

    assert color.key("Hello") == "[yellow]Hello[/yellow]"
    assert color.type("str") == "[magenta]str[/magenta]"
    assert color.arrow("=>") == "[green]=>[/green]"
    assert color.value("uuid") == "[cyan]uuid[/cyan]"

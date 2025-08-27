from app.utils import camel_case_to_snake_case


def test_camel_case_to_snake_case():
    result = camel_case_to_snake_case("SnakeCase")
    assert result == "snake_case"

from pydantic.main import BaseModel


def to_camel_case(string: str) -> str:
    ret = "".join(word.capitalize() for word in string.split("_"))
    return ret[0].lower() + ret[1:]


class Model(BaseModel):
    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True

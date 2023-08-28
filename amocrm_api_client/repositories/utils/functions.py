import typing as t

from pydantic import BaseModel


__all__ = ["make_query_parameters"]


def make_query_parameters(
    _with: t.Optional[t.Collection[str]] = None,
    page: int = 1,
    limit: int = 250,
    query: t.Optional[t.Union[str, int]] = None,
) -> t.Mapping[str, t.Any]:
    str_with = None

    if _with is not None:
        str_with = ",".join(_with)

    params = {
        "with": str_with,
        "page": page,
        "limit": limit,
        "query": query,
    }
    clear_params = {k: v for k, v in params.items() if v is not None}
    return clear_params


def build_model(
    model_type: t.Type[BaseModel],
    data: t.Mapping[str, t.Any],
) -> BaseModel:
    return model_type(**data)

def build_models(
    model_type: t.Type[BaseModel],
    data: t.Mapping[str, t.Any],
) -> t.Collection[BaseModel]:
    return [model_type(**item) for item in data]

from typing import Any, Optional, Union, Iterable


def substr(input: str, begin: Optional[int] = None, end: Optional[int] = None) -> str:
    begin = begin or 0
    end = end or len(input)

    return input[begin:end]


def addPrefix(
    input: str, prefix: Optional[str] = None, delim: Optional[str] = None
) -> str:
    prefix = prefix or ""
    delim = delim or ":"

    if prefix:
        return f"{prefix}{delim}{input}"
    return input


def rmPrefix(input: str, delim: Optional[str] = None) -> str:
    delim = delim or ":"
    return input.split(delim)[-1]


def replPrefix(
    input: str, prefix: Optional[str] = None, delim: Optional[str] = None
) -> str:
    result = rmPrefix(input, delim=delim)
    return addPrefix(result, prefix=prefix, delim=delim)


def wrap(input: str, start: Optional[Any] = None, end: Optional[Any] = None) -> str:
    if not start:
        return input

    end = end or start
    return f"{start}{input}{end}"


def joinSafe(input: Union[str, Iterable[str]], delim: Optional[str] = None) -> str:
    delim = delim or ":"

    if isinstance(input, str):
        return input
    return delim.join(input)


# NOTE: this filter is override the built-in Jinja2's join filter. We will handle the join on python code
def join(input: Iterable, delim: str) -> Iterable:
    return input


all_filters = [substr, addPrefix, rmPrefix, replPrefix, wrap, joinSafe, join]

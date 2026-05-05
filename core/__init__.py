class PromptNotConfiguredError(RuntimeError):
    pass


def safe_format(template: str, **kwargs) -> str:
    """Substitute {key} placeholders in a prompt template without str.format().

    str.format() raises KeyError/ValueError when the template contains literal
    { } characters (e.g. JSON examples in user-authored prompts). This helper
    only replaces the exact patterns we supply and leaves all other braces alone.
    """
    result = template
    for key, value in kwargs.items():
        result = result.replace(f"{{{key}}}", str(value))
    return result

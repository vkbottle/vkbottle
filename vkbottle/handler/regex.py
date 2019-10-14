import re


def vbml_parser(text, f_pattern='{}'):
    """
    Allow to generate REGEX patterns for message matching
    :param text: Text in VBML
    :param f_pattern:
    :return:
    """
    # Make whole text re-invisible
    escape = {ord(x): '\\' + x for x in r'\.*+?()[]|^$'}

    # Find all arguments with validators
    typed_arguments = re.findall(r'(<([a-zA-Z0-9_]+)+:.*?>)', text.translate(escape))
    validation: dict = {}

    # Save validators of validated arguments
    for p in typed_arguments:
        validators = re.findall(r':([a-zA-Z0-9_]+)+', p[0])
        validation[p[1]] = dict()

        # Get arguments of validators
        for validator in validators:
            arguments = re.findall(':' + validator + r'\\\[([a-zA-Z1-9|]+)+\\\]', p[0])
            validation[p[1]][validator] = arguments

        # Delete arguments from regex
        text = re.sub(':.*?>', '>', text.translate(escape))

    pattern = re.sub(r'(<.*?>)',  r'(?P\1.*)', text.translate(escape))
    return re.compile(f_pattern.format(pattern)), validation


def re_parser(pattern):
    return re.compile(pattern)

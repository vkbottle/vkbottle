import re


def vbml_parser(text, f_pattern='{}'):
    """
    Allow to generate REGEX patterns for message matching
    :param text: Text in VBML
    :param f_pattern:
    :return:
    """

    escape = {ord(x): '\\' + x for x in r'\.*+?()[]|^$'}
    typed_arguments = re.findall(r'(<([a-zA-Z0-9_]+)+:.*?>)', text.translate(escape))
    validators: dict = {}

    for p in typed_arguments:
        validators[p[1]] = re.findall(r':([a-zA-Z0-9_]+)+', p[0])
        text = re.sub(':.*?>', '>', text.translate(escape))

    pattern = re.sub(r'(<.*?>)',  r'(?P\1.*)', text.translate(escape))
    return re.compile(f_pattern.format(pattern)), validators


def re_parser(pattern):
    return re.compile(pattern)

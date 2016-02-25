import re


def pluralize(name):
    # getting the name like this will break down as soon as we add
    # resources that don't just append an s for pluralization. Fix when
    # that problem arises.
    return name.lower() + 's'


def singularize(name):
    return name[:-1]


def underscore_to_titlecase(value):
    def titlecase():
        yield str.lower
        while True:
            yield str.capitalize
    c = titlecase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))


cap_re = re.compile(r'(.)([A-Z][a-z]+)')
all_re = re.compile(r'([a-z0-9])([A-Z])')
def titlecase_to_underscore(value):
    s1 = cap_re.sub(r'\1_\2', value)
    return all_re.sub(r'\1_\2', s1).lower()

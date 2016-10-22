def generate_repr_method(*columns):
    def __repr__(self):
        return '<{name}{space}{cols}>'.format(
            name=type(self).__name__,
            space=' ' if len(columns) else '',
            cols=' '.join(('{c}={{self.{c}}}'.format(c=c) for c in columns)),
        ).format(self=self)

    return __repr__


def generate_str_method(*columns):
    def __str__(self):
        return (
            ' '.join(('{{self.{c}}}'.format(c=c) for c in columns))
        ).format(self=self)

    return __str__

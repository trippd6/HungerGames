from pprint import pformat


class ValidationError(RuntimeError):
    pass


def validate_submitted_data(config, data):
    for field in config:
        if field['type'] == 'Select':
            validate_select_field(field, data)
        if field['type'] == 'Integer':
            validate_integer_field(field, data)
        if field['type'] == 'Boolean':
            validate_boolean_field(field, data)


def validate_select_field(field, data):
    if field['id'] in data:
        value = data[field['id']]
        valid_choices = field['options']['choices']
        if value not in valid_choices:
            raise ValidationError(
                    "Invalid choice %s for select field, valid options "
                    "are %s" % (pformat(value), pformat(valid_choices)))
    elif field['required']:
        raise ValidationError("Required field (%s) was missing" % field['name'])


def validate_integer_field(field, data):
    if field['id'] in data:
        value = data[field['id']]
        min_ = field['options'].get('min', None)
        if min_ is not None and min_ < value:
            raise ValidationError("Integer %s was below minimum allowed value "
                    "of %s" % (pformat(value), pformat(min_)))
    elif field['required']:
        raise ValidationError("Required field (%s) was missing" % field['name'])


def validate_integer_field(field, data):
    if field['id'] in data:
        value = data[field['id']]
        try:
            cast_value = bool(value)
            if cast_value is not value:
                raise ValidationError("Value supplied %s was not a boolean" %
                        pformat(value))
        except:
            raise ValidationError("Cannot cast %s to type bool" %
                    pformat(value))
    elif field['required']:
        raise ValidationError("Required field (%s) was missing" % field['name'])

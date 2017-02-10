import unittest
from hunger_games.validation import validate_submitted_data, ValidationError

class TestValidation(unittest.TestCase):
    config = [
        {
            'id': 5,
            'name': 'Example Select Field',
            'type': 'Select',
            'options': {'choices': ['foo', 'bar', 'baz']},
            'required': True,
        },
        {
            'id': 7,
            'name': 'Example Integer Field',
            'type': 'Integer',
            'options': {'min': 4, 'max': 11},
            'required': True,
        },
        {
            'id': 12,
            'name': 'Example Boolean Field',
            'type': 'Boolean',
            'options': {'default': True},
            'required': False,
        },
    ]


    data = {
        5: 'baz',
        7: 23,
        12: True,
    }

    def test_validation(self):
        self.assertEquals(None, validate_submitted_data(self.config, self.data))

    def test_integer_too_small(self):
        bad_data = {**self.data, 7: 0}
        try:
            validate_submitted_data(self.config, bad_data)
            self.fail("Didn't raise exception as expected")
        except ValidationError as e:
            self.assertEquals("Integer 0 was below minimum allowed value of 4", e.args[0])

    def test_invalid_select(self):
        bad_data = {**self.data, 5: 'taco'}
        try:
            validate_submitted_data(self.config, bad_data)
            self.fail("Didn't raise exception as expected")
        except ValidationError as e:
            self.assertEquals("Invalid choice 'taco' for select field, valid "
                    "options are ['foo', 'bar', 'baz']", e.args[0])

class Validator:

    lens_text = {
        'achievement': 1000,
        'boss_review': 1000,
        'coworker': 1000,
        'form': 1000,
        'project_description': 2000,
        'fullname': 255,
                 }

    def validate_text(self, text: str, type_text: str) -> bool:
        """  """
        if isinstance(text, str):
            if len(text) <= self.lens_text[type_text]:
                return True
            raise TextValidationError(len(text), self.lens_text[type_text])
        raise InvalidTypeValidationError(type(text), str)


class ValidationError(ValueError):
    pass


class TextValidationError(ValidationError):
    pass


class InvalidTypeValidationError(ValidationError):
    pass

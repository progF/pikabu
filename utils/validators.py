from django.core.exceptions import ValidationError
from utils.constants import MALE, OTHER, BY_TIME_DESC, BY_TIME_ASC


def profile_gender(value):
    if OTHER > value < MALE:
        raise ValidationError('Invalid gender value: [1, 2, 3].')


def comment_sort(value):
    if BY_TIME_ASC > value < BY_TIME_DESC:
        raise ValidationError('Invalid comment sort value: [1, 2].')


def validate_image(image):
    size = image.file.size
    megabyte_limit = 3.0
    if size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max image size is %sMB" % str(megabyte_limit))
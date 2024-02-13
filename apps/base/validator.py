# validator, validation -- tekshirish

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_file_types(value):
    """
    User input qilgayotgan fileni turini tekshiradi
    (image, Video, Gif)
    """

    allowed_types = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'mkv']

    validator = FileExtensionValidator(allowed_types, message=(
        "You can only upload for Image(jpg, jpeg, png, gif). Video(mp4, avi, mov, mkv)"
    ))

    try:
        validator(value)
    except ValidationError as p:
        raise ValidationError(
            f"You have error with uploading file. Detailed error is here: {p}")

from typing import Annotated

from pydantic_extra_types.phone_numbers import PhoneNumberValidator

PhoneStr = Annotated[str, PhoneNumberValidator(supported_regions=['VN'], default_region='VN')]
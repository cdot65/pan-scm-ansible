# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

from typing import Any, Dict, Union


def serialize_response(response: Any) -> Union[Dict, Any]:
    """
    Convert API response object to Ansible-compatible format.

    This function handles the conversion of response objects to dictionary format,
    ensuring proper serialization of special types like UUID fields. It maintains
    compatibility with Ansible's expected data structures.

    Args:
        response: The response object to serialize. Can be a Pydantic model
                 or any other response type.

    Returns:
        Union[Dict, Any]: The serialized response as a dictionary if the input
        was a model object, otherwise returns the original response unchanged.

    Examples:
        >>> response = SomeModel(id=UUID('123e4567-e89b-12d3-a456-426614174000'))
        >>> serialize_response(response)
        {'id': '123e4567-e89b-12d3-a456-426614174000', ...}
    """
    if hasattr(response, 'model_dump'):
        data = response.model_dump()
        # Convert UUID to string
        if 'id' in data and data['id']:
            data['id'] = str(data['id'])
        return data
    return response

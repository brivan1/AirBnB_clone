#!/usr/bin/python3
"""module creates User class"""

from models.base_model import BaseModel


class City(BaseModel):
    """Class for handeling city objects"""

    state_id = ""
    name = ""

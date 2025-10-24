from abc import ABC

from pydantic import BaseModel


class Component(ABC, BaseModel):
    pass

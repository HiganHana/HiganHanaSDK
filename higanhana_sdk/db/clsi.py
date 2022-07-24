
from dataclasses import dataclass
import dataclasses
from functools import cached_property


@dataclass
class DBClsInterface:
    @cached_property
    def dataclassNames(self):
        return [k.name for k in dataclasses.fields(self)]

    def updateVars(self, **kwargs):
        for k, v in kwargs.items():
            if k not in self.dataclassNames:
                raise ValueError(f"{k} is not a valid field for {self.__class__.__name__}")
            setattr(self, k, v)
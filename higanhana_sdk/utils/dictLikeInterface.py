from abc import abstractmethod, abstractproperty
import typing

class DictLikeInterface:
    @abstractproperty
    def hasInit(self) -> bool:
        return False

    @abstractmethod
    def __getitem__(self, key: str) -> str:
        return None

    @abstractmethod
    def __setitem__(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def __delitem__(self, key: str) -> None:
        pass

    @abstractmethod 
    def __contains__(self, key: str) -> bool:
        return False

    @abstractmethod
    def keys(self) -> str:
        return None

    @abstractmethod
    def values(self):
        return None

    @abstractmethod
    def items(self) -> typing.Union[str, typing.Any]:
        return None

    @abstractmethod
    def filterPrefix(self, key: str):
        return None

    @abstractmethod
    def copyTo(self, other: typing.Union['DictLikeInterface',dict]) -> None:
        if not isinstance(other, (DictLikeInterface, dict)):
            raise TypeError("other must be a DictLikeInterface or dict")

        if other == dict:
            target = {}
        else:
            target = other()
            
        for key, val in self.items():
            target[key] = val
        return target

       
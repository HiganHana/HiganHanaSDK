
from dataclasses import dataclass
import typing
from higanhana_sdk.utils.dictLikeInterface import DictLikeInterface

@dataclass(frozen=True, init=False)
class ReplDB(DictLikeInterface):
    def __init__(self) -> None:
        try:
            # 
            from replit import db # type: ignore
            object.__setattr__(self, "db", db)
        except:
            object.__setattr__(self, "db", None)

    @property
    def hasInit(self) -> bool:
        return self.db is not None

    def __getitem__(self, key: str) -> str:
        try:
            return self.db[key]
        except:
            return None

    def __setitem__(self, key: str, value: str) -> None:
        try:
            self.db[key] = value
        except:
            pass
    
    def __delitem__(self, key: str) -> None:
        try:
            del self.db[key]
        except:
            pass

    def __contains__(self, key: str) -> bool:
        try:
            return key in self.db
        except:
            return False

    def keys(self) -> str:
        try:
            keys = list(self.db.keys())
            for key in keys:
                yield key
        except:
            pass

    def values(self):
        try:
            for key in self.keys():
                yield self.db[key]
        except:
            pass

    def items(self) -> typing.Union[str, typing.Any]:
        try:
            for key in self.keys():
                yield key, self.db[key]
        except:
            pass

    @typing.overload
    def filterPrefix(self, key: str):
        pass

    @typing.overload
    def filterPrefix(self, key: str, seq : typing.Iterable):
        pass

    def filterPrefix(self, key, seq = None):
        if seq is None:
            try:
                seq = self.db.prefix(key)
            except:
                return
        else:
            seq = [x for x in seq if x.startswith(key)]

        for item in seq:
            yield item

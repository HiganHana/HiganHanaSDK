from functools import cached_property
import os
from typing import overload
import json

def trySerialize(key, val):
    try:
        json.dumps({key: val})
        return {key: val}
    except:
        return None

def _actual_serialize(base):
    try:
        json.dumps(base)
        return base
    except:
        new_ret = {}
        for key, val in base.items():
            if isinstance(val, dict):
                new_ret[key] = _actual_serialize(val)
            elif (s := trySerialize(key, val)) is not None:
                new_ret.update(s)

        return new_ret


class _GlobalConfig(type):
    _configs = {}
    _focuser = {}

    def _get_default_space(cls):
        if "_" not in cls._configs:
            cls._configs["_"] = {}

        return cls._configs["_"]

    def _get_space(cls, space: str, create: bool = False):
        if space is None:
            return cls._get_default_space()

        if space not in cls._configs:
            if not create:
                return None

            cls._configs[space] = {}

        return cls._configs[space]

    def _load_source(cls, source_path: str):
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"{source_path} not found")

        with open(source_path) as f:
            configs = json.load(f)

        cls._configs.update(configs)    

    def _load_source_with_env(cls, source_path: str, env : str):
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"{source_path} not found")

        with open(source_path) as f:
            configs = json.load(f)

        env_dict = cls._get_space(env, True)
        env_dict.update(configs)

    def __call__(cls, *args, **kwargs):
        if (len(args) == 1 and len(kwargs) == 0):
            env = "_"
            env_dict = cls._get_default_space()
            cls._load_source(args[0])
        elif ("source_path" in kwargs and len(kwargs) == 1):
            env = "_"
            env_dict = cls._get_default_space()
            cls._load_source(kwargs["source_path"])
        elif (len(args) == 2 and len(kwargs) == 0):
            env = args[0]
            cls._load_source_with_env(args[0], args[1])
            env_dict = cls._get_space(args[1])
        elif ("source_path" in kwargs and "env" in kwargs and len(kwargs) == 2):
            env = kwargs["env"]
            cls._load_source_with_env(kwargs["source_path"], kwargs["env"])
            env_dict = cls._get_space(kwargs["env"])
        elif "env" in kwargs:
            env = kwargs["env"]
            env_dict = cls._get_space(kwargs.pop("env"), True)
            env_dict.update(kwargs)
        else:
            env = "_"
            env_dict = cls._get_space("_", True)
            env_dict.update(kwargs)
            
        if env not in cls._focuser:
            instance = super().__call__()
            cls._focuser[env] = instance
            instance._focus_space = env_dict
        
        return cls._focuser[env]
    
        
class GlobalConfig(metaclass=_GlobalConfig):
    @overload
    def __init__(self, source_path : str) -> None: pass

    @overload
    def __init__(self, source_path : str, env : str) -> None: pass

    @overload
    def __init__(self, env: str = None, **kwargs): pass

    def __init__(self, *args, **kwargs) -> None:
        self._focus_space = None

        
    @cached_property
    def _default_space(self):
        return self.__class__._get_default_space()

    def __getattr__(self, key: str) -> str:
        if key.startswith("_"):
            return super().__getattribute__(key)

        if key in self._focus_space:
            return self._focus_space[key]

        if self._default_space is not self._focus_space and key in self._default_space:
            return self._default_space[key]

    def __setattr__(self, key, val) -> None:
        if key.startswith("_"):
            super().__setattr__(key, val)
            return

        self._focus_space[key] = val

    def __delattr__(self, key) -> None:
        if key.startswith("_"):
            super().__delattr__(key)
            return

        del self._focus_space[key]

    def __contains__(self, key):
        return key in self._focus_space

    def _serializeScope(self):
        return _actual_serialize(self._focus_space)

    @classmethod
    def _serialize(cls):
        return _actual_serialize(cls._configs)
                

CONFIG = GlobalConfig()
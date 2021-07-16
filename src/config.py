import yaml
import logging

logger = logging.getLogger(__name__)

with open("config.yml", "r") as f:
    _CONFIG = yaml.safe_load(f)


class _Construct:
    def __init__(cls, name, bases, dct):
        if cls.parent is not None:
            setattr(globals()[cls.parent], cls.__name__, cls)

        for attribute in cls.__annotations__.keys():
            try:
                if attribute == "parent":
                    continue

                if cls.parent is not None:
                    setattr(cls, attribute, _CONFIG[cls.parent.lower()][cls.__name__.lower()][attribute])
                else:
                    setattr(cls, attribute, _CONFIG[cls.__name__.lower()][attribute])
            except KeyError as err:
                logger.critical(f"Failed to load attribute {attribute} from section {cls.__name__.lower()}")
                raise AttributeError(attribute) from err


class Environment(metaclass=_Construct):
    parent = None

    vision: int
    grid_size: int


class Rewards(metaclass=_Construct):
    parent = "Environment"

    death: int
    apple: int
    timestep: int
    towards_apple: int
    away_from_apple: int


class Vision(metaclass=_Construct):
    parent = "Environment"

    type: str
    directions: int


class Mode(metaclass=_Construct):
    parent = None

    train: bool
    agent_play: bool
    teach: bool
    user_play: bool


class Window(metaclass=_Construct):
    parent = None

    active: bool
    size: bool
    title: str


class Colours(metaclass=_Construct):
    parent = "Window"

    grid: list[list[int]]
    snake: list[int]
    apple: list[int]


class Misc(metaclass=_Construct):
    parent = None

    debug: bool

from pydantic import RootModel, Field


class ColorMap(RootModel[list[tuple[str, str]]]):
    root: list[tuple[str, str]] = Field(
        default_factory=list,
        description="list of characters and their corresponding colors.",
    )

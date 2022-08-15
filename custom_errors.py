class IncorrectBaseGameSetupError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FailedToReadFileError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class SetupNotMatchingRulesError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidFigurePositionError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class MoreFiguresOnOneTileError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
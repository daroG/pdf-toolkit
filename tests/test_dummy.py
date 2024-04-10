class Dummy:
    def __init__(self) -> None:
        self.attribute = True


def test_true():
    dummy = Dummy()
    assert dummy.attribute

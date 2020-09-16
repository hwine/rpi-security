import pytest

def test_pytest()->None:
    pass

def fred(a:int=0, b:str="") -> str:
    """Everyone knows fred

    Args:
        a (int, optional): number of times to repeat b. Defaults to 0.
        b (str, optional): string to repeat. Defaults to "".

    Returns:
        str: replicated string
    """
    return b * a

def test_fred() -> None:
    a = fred()
    assert len(a) == 0
    return
    

    

if __name__ == "__main__":
    pass

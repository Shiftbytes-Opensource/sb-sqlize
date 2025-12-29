from sqlize import functions

def test_sqlize():
    assert isinstance(functions.sqlize("./jsonfile.json"), str)
from statement_import.natwest_csv import read_csv


def test_csv_read():
    data = read_csv("tests/test_natwest.csv")
    assert len(data) == 1

    row = data[0]
    assert row[0] == "04/01/2022"
    assert row[1] == "D/D"
    assert row[2] == "AVIVA LIFE"
    assert row[3] == "-9.39"
    assert row[4] == "25318.58"
    assert row[5] == "CHUNG M/2010"
    assert row[6] == "604008-32798695"

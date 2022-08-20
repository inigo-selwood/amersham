from amersham import table


def test_table():

    table_ = [
        ["the", "quick", "brown"],
        ["fox", "jumped", "over"],
        ["the", "lazy", "dog"],
    ]

    # Default delimiter & newline
    answer = """the quick  brown
fox jumped over
the lazy   dog"""
    assert(table.serialize(table_) == answer)

    # Custom delimiter & newline
    answer = """the  quick   brown
  fox  jumped  over
  the  lazy    dog"""
    assert(table.serialize(table_, delimiter="  ", newline="\n  ") == answer)
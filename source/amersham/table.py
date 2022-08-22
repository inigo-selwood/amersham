def serialize(table: list, delimiter = " ", newline = "\n") -> str:

    # Evaluate shape
    row_count = len(table)
    if row_count == 0:
        return ""
    column_count = len(table[0])

    # Calculate max column widths
    widths = [0] * column_count
    last_columns = [0] * row_count
    for row_index in range(row_count):
        row = table[row_index]

        if len(row) != column_count:
            raise Exception("inconsistent table shape")

        for column_index in range(column_count):

            value = row[column_index]
            if not isinstance(value, str):
                raise Exception("table contains non-string value")

            column_width = widths[column_index]
            value_width = len(value)
            widths[column_index] = max(column_width, value_width)

            if value_width:
                last_columns[row_index] = column_index
    
    # Pad values, serialize result
    rows = []
    for row_index in range(row_count):

        columns = []
        for column_index in range(column_count):

            # Skip the row if there are no values
            if widths[column_index] == 0:
                continue

            value = table[row_index][column_index]
            width = len(value)

            padding = ""
            last_column_index = last_columns[row_index]
            if column_index < last_column_index:
                padding = " " * (widths[column_index] - width)
            if column_index <= last_column_index:
                columns.append(f"{value}{padding}")
                
        rows.append(delimiter.join(columns))
    return newline.join(rows)
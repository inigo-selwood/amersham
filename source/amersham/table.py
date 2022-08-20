def serialize(table: list, 
        delimiter: str = " ", 
        newline: str = "\n") -> str:
    
    ''' Spaces columns of a 2D array ("table") 
    
    Arguments
    ---------
    table: the table to format
    delimiter: string between each column
    newline: string between each row
    
    Returns
    -------
    table: the formatted table

    Usage
    -----

    ```
    >>> table = [
    ...     ["the", "quick", "brown"],
    ...     ["fox", "jumped", "over"],
    ...     ["the", "lazy", "dog"],
    ... ]
    >>> print(serialize(table))
    the quick  brown
    fox jumped over
    the lazy   dog
    ```
    '''
    
    # Evaluate shape
    row_count = len(table)
    if row_count == 0:
        return ""
    column_count = len(table[0])

    # Calculate max column widths
    widths = [0] * column_count
    for row in table:

        if len(row) != column_count:
            raise Exception("inconsistent table shape")

        for column_index in range(column_count):

            value = row[column_index]
            width = widths[column_index]
            widths[column_index] = max(width, len(value))
    
    # Pad values, serialize result
    rows = []
    for row in table:

        columns = []
        for column_index in range(column_count):
            value = row[column_index]
            width = len(value)

            padding = ""
            if column_index + 1 < column_count:
                padding = " " * (widths[column_index] - width)
            columns.append(value + padding)
                
        rows.append(delimiter.join(columns))
    
    return newline.join(rows)
    
def create_table(data):
    table_header = ""
    table_rows = ""

    if data:  # Check if data list is not empty
        if isinstance(data[0], dict):
            table_header = "<tr>" + "".join(f"<th>{header}</th>" for header in data[0].keys()) + "</tr>"

        for row in data:
            table_cells = ""
            for value in row.values():
                table_cells += f"<td>{value}</td>"
            table_rows += f"<tr>{table_cells}</tr>"

    table = f"""
    <table border="1" cellpadding="5">
        <thead>
            {table_header}
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """

    return table

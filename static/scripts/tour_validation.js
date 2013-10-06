function validateStartColumn() {
        var columns = document.getElementById("columns");
        var columns_value = columns.options[columns.selectedIndex].value;
        var start_column = document.getElementById("starting_column");
        var sc_value = start_column.options[start_column.selectedIndex].value;
        //alert("columns: " + columns_value + " starting column: " + sc_value);
        if (parseInt(sc_value) > parseInt(columns_value)) {
                alert("Your starting column does not fit on the board. Please choose a number less than or equal to the number of columns on the board")
                start_column.value = columns_value;
        }
}
function validateStartRow() {
        var rows = document.getElementById("rows");
        var rows_value = rows.options[rows.selectedIndex].value;
        var start_row = document.getElementById("starting_row");
        var sr_value = start_row.options[start_row.selectedIndex].value;
        //alert("columns: " + columns_value + " starting column: " + sc_value);
        if (parseInt(sr_value) > parseInt(rows_value)) {
                alert("Your starting row does not fit on the board. Please choose a number less than or equal to the number of rows on the board")
                start_row.value = rows_value;
        }
}
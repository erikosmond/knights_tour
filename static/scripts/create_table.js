//This is not ready yet, I need to pass in parameters and not just set the table width and height with django
        var cell_index = 0;
	//cells = ["1.1", "2.3", "1.5", "3.4", "5.5", "4.3", "5.1", "3.2", "4.4", "5.2", "3.1", "1.2", "2.4", "4.5", "5.3", "4.1", "2.2", "1.4", "3.5", "5.4", "4.2", "2.1", "1.3", "2.5", "3.3"];
	cells = "{{ cells }}".replace(/&#39;/g,"\"").substring(1,parseInt("{{ len_positions }}"))
        cells_array = JSON.parse("[" + cells + "]")
        var sleep = 1000
	function setValues() {
	    var previous = false;
	    setTimeout(function () {

		document.getElementById(cells_array[cell_index]).innerHTML = "<img width=\"40px\" src=\"/static/images/Chess_nlt60.png\">";
		if (cell_index>0) {
		    document.getElementById(cells_array[cell_index-1]).innerHTML =  cell_index-1;
		}
		cell_index++;
		if (cell_index < cells_array.length) {
		    setValues();
		}
		sleep -= 50
		sleep = Math.max(sleep,150)
	    }, sleep)
	}
	
	function tableCreate() {
        var numRows = parseInt("{{ rows }}"),
            numColumns = parseInt("{{ columns }}"),
            body = document.body,
            tbl = document.createElement('table'),
            tbdy = document.createElement('tbody');
    
        tbl.style.height = "{{ table_height }}".replace(/&quot;/g,"")
        tbl.style.width = "{{ table_width }}".replace(/&quot;/g,"")
        for(var i=1; i<=numRows; i++) {
            var tr = document.createElement('tr');
            for(var j=1; j<=numColumns; j++) {
                var td = document.createElement('td');
                td.style.height = "{{ cell_size }}".replace(/&quot;/g,"");
                td.style.width = "{{ cell_size }}".replace(/&quot;/g,"");
                td.id = i+"."+j;
                (i+j) % 2 == 0 ? td.className = "EvenSquare" : td.className = "OddSquare";
                tr.appendChild(td)
            }
            tbdy.appendChild(tr);
        }
        tbl.appendChild(tbdy);
        body.appendChild(tbl)
        setValues();
    }
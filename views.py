from django.http import HttpResponse
from django.template import loader, RequestContext

from django.shortcuts import redirect, render_to_response

from chess_forms import StartTourForm

from app.tour import Tour
from app.pieces import GameError

def choose_tour(request):
    #return HttpResponse("Hello, Notes")
    if request.method=="POST":
        print "Received POST"
        form=request.POST#StartTourForm(request.POST)
        if form:#.is_valid():
            print "Form is valid",
            # user registration or login code
            rows = int(request.POST.get("rows",None))
            columns = int(request.POST.get("columns",None))
            starting_row = request.POST.get("starting_row",None)
            starting_column = request.POST.get("starting_column",None)
            closed = request.POST.get("tour_type",False)
            if closed == "Closed":
                closed = True
            #get speed and size from the user as well
            verbosity = 0
            move_limit = 150000
            if not rows or not columns or not starting_row or not starting_column:
                return HttpResponse("One or more fields are missing")
            starting_location = str(starting_row) + '.' + str(starting_column)
            print "Starting Tour"
            print "closed = ", closed
            try:
                t = Tour(rows, columns, starting_location, verbosity, closed, move_limit=move_limit)
                knight, count, board = t.run()
            except GameError:
                template=loader.get_template("choose_tour.html")
                rc=RequestContext(request,{'Error':'No solution could be found in ' + str(move_limit) + ' moves, please try again. The number of moves attempted in solving the puzzle has been capped to reduce server load.', "form":form})
                return HttpResponse(template.render(rc))  
                #return HttpResponse("No solution available")
                #instead return the index page but with an error message - please try again
            
            positions = []
            for p in knight.visited_positions:
                positions.append(p.str_coordinate)
            
            column_var = 19 - int(columns)
            cell_s = min(column_var*12,90)
            cell_size = r'"' + str(cell_s) + r'"px'
            table_width = r'"' + str(cell_s * columns + columns) + r'"px'
            table_height = r'"' + str(cell_s * rows + rows) + r'"px'
            template=loader.get_template("tour.html")
            rc=RequestContext(request,{'cells':positions, "rows":rows, "columns":columns,
                                       "len_positions":len(str(positions))-1,
                                       "cell_size":cell_size,
                                       "table_width":table_width,
                                       "table_height":table_height,
                                       "count":count
                                       })
            return HttpResponse(template.render(rc)) 
            
            #return redirect(dashboard)
        else:
            print "Form is not valid"
            for error in form.errors:
                print error
            template=loader.get_template("choose_tour.html")
            rc=RequestContext(request,{'Error':'There was an error loading the page', "form":form})
            return HttpResponse(template.render(rc))            
    else:
        template=loader.get_template("choose_tour.html")
        rc=RequestContext(request,{'username':"Erik"})#, "form":StartTourForm()}) #HtmlTourForm
        return HttpResponse(template.render(rc))
    
def index(request):
    template=loader.get_template("index.html")
    rc=RequestContext(request,{'username':"Erik"})
    return HttpResponse(template.render(rc))
    
from django.http import HttpResponse
from django.template import loader, RequestContext

from django.shortcuts import redirect, render_to_response

from chess_forms import StartTourForm

from app.tour import Tour

def index(request):
    #return HttpResponse("Hello, Notes")
    if request.method=="POST":
        print "Received POST"
        form=StartTourForm(request.POST)
        if form.is_valid():
            print "Form is valid",
            # user registration or login code
            rows = request.POST.get("rows",None)
            columns = request.POST.get("columns",None)
            starting_row = request.POST.get("starting_row",None)
            starting_column = request.POST.get("starting_column",None)
            closed = False #add this value from the form then use it here
            #get speed and size from the user as well
            verbosity = 0
            if not rows or not columns or not starting_row or not starting_column:
                return HttpResponse("Username or password not present")
            starting_location = str(starting_row) + '.' + str(starting_column)
            print "Starting Tour"
            t = Tour(rows, columns, starting_location, verbosity, closed)
            knight, count, board = t.run()
            
            
            positions = []
            for p in knight.visited_positions:
                positions.append(p.str_coordinate)
            
            
            
            template=loader.get_template("tour.html")
            rc=RequestContext(request,{'cells':positions, "rows":rows, "columns":columns, "len_positions":len(str(positions))-1})
            return HttpResponse(template.render(rc)) 
            
            #return redirect(dashboard)
        else:
            print "Form is not valid"
            template=loader.get_template("index.html")
            rc=RequestContext(request,{'username':"Erik", "form":form})
            return HttpResponse(template.render(rc))            
    else:
        template=loader.get_template("index.html")
        rc=RequestContext(request,{'username':"Erik", "form":StartTourForm()})
        return HttpResponse(template.render(rc))
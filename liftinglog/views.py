from django.shortcuts import render_to_response, get_object_or_404
from liftinglog.models import Log, Lift
from django.contrib.auth import authenticate, login, logout

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from forms import LogForm, LiftFormSet



def index(request):
    
    if request.user.is_authenticated():
                
        l = Log.objects.filter(user=request.user).order_by('-pub_date')
        # List of Logs belonging to the user, ordered by Pub_date
        lifts = Lift.objects.filter(log__user=request.user).values('name').distinct()[:5]
        # List of all Lifts objects belonging to a current user log with the value name.
        # Distinct so we get only one of each lift in the list
        return render_to_response('index.html', {'listlog': l, 'lifts': lifts}, context_instance=RequestContext(request))
    
    else: 
        data = {}
        # Empty data array because render_to_response needs 3 arguments.
        return render_to_response('index.html', data, context_instance=RequestContext(request))

def about(request):
    data = {}
    return render_to_response('about.html', data, context_instance=RequestContext(request))

def detail(request, log_id):
    # Get object with correct id
    try: 
        l = Log.objects.get(pk=log_id, user=request.user)
    except Log.DoesNotExist:
        HttpResponseRedirect('/myliftinglog/')
    
    try:
        nextl = l.get_next_by_pub_date(user=request.user)
    except Log.DoesNotExist:
        nextl = None
    try:
        prel = l.get_previous_by_pub_date(user=request.user)
    except Log.DoesNotExist:
        prel = None
    return render_to_response('detail.html', {'log': l, 'oldlog':prel, 'newlog':nextl}, context_instance=RequestContext(request))

def progress(request, lift):
    
    # Get all objects ordered by their Log pub date's, filtered by user and by the name of the lift.
    s = (Lift.objects.order_by('log__pub_date').filter(log__user=request.user).filter(name=lift))
    return render_to_response('progress.html', {'data': s, 'lift':lift}, context_instance=RequestContext(request))

def registration(request):
    
    # If user is already logged in, Redirect to Index
    if request.user.is_authenticated():
        return HttpResponseRedirect('/myliftinglog/')
    
    # If user just submitted the form, Register the user.
    if request.method == 'POST':
        
        errors = []
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # Create the users
        user = User.objects.create_user(username, email, password)
        
        return HttpResponseRedirect('/myliftinglog/')
        
    # If the user is not logged in, show the form     
    else:
        return render_to_response('register.html', context_instance=RequestContext(request)) 
    
def addLog(request):
    
    # If user is logged in
    if request.user.is_authenticated():
        # And submitted the form
        if request.method == 'POST':
            # Get form info
            form = LogForm(request.POST)
            if form.is_valid():
                # Save the log without commit so its not saved in database
                log = form.save(commit=False)
                log.user = request.user
                # Get info grom FormSet, our created log as instance
                lift_formset = LiftFormSet(request.POST, instance=log)
                if lift_formset.is_valid():
                    # Finally save the log
                    log.save()
                    # Save formset attached to log
                    
                    lift_formset.save()
                    
                    return HttpResponseRedirect('/myliftinglog/')
                
        # if user did not submit form, render the form  
        else:
            form = LogForm()
            lift_formset = LiftFormSet(instance=Log())
        
            return render_to_response('addlog.html', {'form': form, 'formset': lift_formset} , context_instance=RequestContext(request))
    
    
    else: return HttpResponseRedirect('/myliftinglog/register')
    
def signin(request):
    
    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/myliftinglog/')
    else:
        return HttpResponseRedirect('/myliftinglog/')
    
    
def signout(request):
    logout(request)
    return HttpResponseRedirect('/myliftinglog/')
    

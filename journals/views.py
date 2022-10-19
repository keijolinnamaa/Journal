from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """The home page for Journal"""
    return render(request, 'journals/index.html')

@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics' : topics}
    return render(request, 'journals/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show single topic identified by id"""
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added') # - for reverse order
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'journals/topic.html', context)
    
@login_required
def new_topic(request):
    """Adding a new topic"""
    if request.method != 'POST':
        form = TopicForm() #No data, create blank form
    else:
        form = TopicForm(data=request.POST) #POST data, process it
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('journals:topics')

    #Show blank or invalid
    context = {'form' : form}
    return render(request, 'journals/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """New entry for particular topic"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)

    if request.method != 'POST':
        form = EntryForm() #No data, blank form
    else:
        form = EntryForm(data=request.POST) #POST data from the request object
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('journals:topic', topic_id=topic_id)

    #Blank or invalid form
    context = {'topic':topic, 'form':form}
    return render(request, 'journals/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Editting entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)
    

    if request.method != 'POST':
        form = EntryForm(instance=entry) #Fill form with current entry
    else:
        form =EntryForm(instance=entry, data=request.POST) # data so process
        if form.is_valid():
            form.save()
            return redirect('journals:topic', topic_id=topic.id)

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'journals/edit_entry.html', context)

def check_topic_owner(request, topic): #Makes sure the topic belongs to the user
    if topic.owner != request.user:
        raise Http404
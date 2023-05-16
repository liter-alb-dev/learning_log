from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_log_app/index.html')

def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404


@login_required
def topics(request):
    """The page to view all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_log_app/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(topic, request)

    entries = topic.entry_set.order_by('date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_log_app/topic.html', context)

@login_required
def new_topic(request):
    """Add new topic"""
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = TopicForm()
        # Display a blank or invalid form.
        context = {'form': form}
        return render(request, 'learning_log_app/new_topic.html', context)
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_log_app:topics')

@login_required
def new_entry(request, topic_id):
    """Add new entry to topic_id"""
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_owner(topic, request)

    if request.method != "POST":
        # No data submitted; create a blank form.
        form = EntryForm()
        # Display a blank or invalid form.
        context = {'form': form, 'topic': topic}
        return render(request, 'learning_log_app/new_entry.html', context)
    else:
        # POST data submitted; process data.
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect(f'learning_log_app:topic', topic_id=topic_id)

@login_required
def edit_entry(request, entry_id):
    """Add new entry to topic_id"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)

    if request.method != "POST":
        # No data submitted; create a blank form.
        form = EntryForm(instance=entry)
        # Display a blank or invalid form.
        context = {'form': form, 'topic': topic, 'entry': entry}
        return render(request, 'learning_log_app/edit_entry.html', context)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'learning_log_app:topic', topic_id=topic.id)

from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.db.models import Count
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.http import HttpResponse
from Boards.models import Board, Topic, Post
from Boards.forms import NewTopicForm, NewReplyForm
from django.contrib.auth.decorators import login_required

class BoardsListView(ListView):
    model = Board
    template_name = 'Boards/BoardsList.html'
    context_object_name = 'boards'

class TopicsListView(ListView):
    template_name = 'Boards/TopicsList.html'
    context_object_name = 'topics'


    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-updated_at').annotate(replies=Count('posts') - 1)
        return queryset

class TopicView(ListView):
    form_class = NewReplyForm
    template_name = 'Boards/Topic.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = Board.objects.get(
            pk=self.kwargs.get('pk')).topics.get(slug=self.kwargs.get('slug')).posts
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        self.topic = get_object_or_404(Topic, slug=self.kwargs.get('slug'))
        return get_list_or_404(queryset)

@login_required
def NewTopic(request,pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = Topic.objects.create(
                subject = form.cleaned_data['subject'],
                board = board,
                starter = request.user
            )
            Post.objects.create(
                message = form.cleaned_data['message'],
                topic = topic,
                created_by = request.user)
            return redirect(reverse('topic_view',kwargs={'pk':board.pk,'slug':topic.slug}))
    else:
        form = NewTopicForm()
    return render(request, 'Boards/NewTopic.html', {'form':form, 'board':board})

@login_required
def NewReply(request,pk,slug):
    board = get_object_or_404(Board, pk=pk)
    topic = get_object_or_404(Topic, slug=slug)
    if request.method == 'POST':
        form = NewReplyForm(request.POST)
        if form.is_valid():
            post = Post.objects.create(
                message = form.cleaned_data['message'],
                topic = topic,
                created_by = request.user)
            return redirect(reverse('topic_view',kwargs={'pk':board.pk,'slug':topic.slug}))
    else:
        form = NewReplyForm()
    return render(request, 'Boards/NewReply.html', {'form':form, 'board':board, 'topic':topic})

def EditReply(request,pk,slug):
    



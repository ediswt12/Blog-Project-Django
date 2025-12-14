from django.shortcuts import render
from .models import Poll, Option

# Create your views here.

def poll_list(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'poll_list.html', {'polls': polls})


def vote_poll(request, poll_id, option_id):
    poll = Poll.objects.all(Poll, id=poll_id)
    option = Option.objects.all(Option, id=option_id, poll=poll)
    
    if request.user in option.votes.all():
        option.votes.remove(request.user)
    else:
        option.votes.add(request.user)
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


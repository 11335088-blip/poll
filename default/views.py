from django.shortcuts import render
from .models import poll,option
from django.views.generic import ListView,DetailView,RedirectView
from django.urls import reverse

# Create your views here.
def poll_list(req):
    polls = poll.objects.all()
    return render(req,'default/list.html',{'poll_list':polls,'msg':'hello!'})

class polllist(ListView):
    model = poll
    
#應用程式名稱/資料模型_list.html
#default/poll_list.html
class PollView(DetailView):
    model = poll

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        option_list = option.objects.filter(poll_id=self.object.id)
        ctx['option_list'] = option_list
        return ctx
    
class PollVote(RedirectView):
    #redirec_url="https://www.google.com"
    def get_redirect_url(self, *args, **kwargs):
        Option = option.objects.get(id=self.kwargs['oid'])
        Option.vote += 1   #option.vote = option.vote+1
        Option.save()
        #return '/poll/{}/',format(Option.poll_id)
        #return f"/poll/{Option.poll_id}"
        #return reverse('poll_view',args=[Option.poll_id])
        return reverse('poll_view',kwargs={'pk':Option.poll_id})


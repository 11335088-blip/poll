from django.shortcuts import render
from .models import poll,option
from django.views.generic import ListView,DetailView,RedirectView,CreateView,UpdateView,DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

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
    
class pollcreate(LoginRequiredMixin, CreateView):
    model = poll
    fields = '__all__' #['subject','desc']
    success_url = reverse_lazy('poll_list')

class polledit(LoginRequiredMixin, UpdateView):
    model = poll
    fields = '__all__' #['subject','desc']   
    def get_success_url(self):
        return reverse_lazy('poll_view', kwargs={'pk':self.object.id})

class optioncreate(LoginRequiredMixin, CreateView):
    model = option
    fields = ['title']   
    def form_valid(self, form):
        form.instance.poll_id = self.kwargs['pid']
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('poll_view', kwargs={'pk':self.kwargs['pid']})
    

class optionedit(LoginRequiredMixin, UpdateView):
    model = option
    fields = ['title']
    pk_url_kwarg = 'oid'

    def get_success_url(self):
        return reverse_lazy ('poll_view', kwargs={'pk':self.object.poll_id})
    #self.object代表的是目前操作的那筆紀錄
    
class polldelete(LoginRequiredMixin, DeleteView):
    model = poll
    success_url = reverse_lazy('poll_list')

class optiondelete(LoginRequiredMixin, DeleteView):
    model = option
    
    def get_success_url(self):
        return reverse_lazy('poll_view', kwargs={'pk':self.object.poll_id})
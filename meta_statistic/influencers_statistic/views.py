from django.views.generic import ListView

from influencers_statistic.models import Statistics


class BaseStatistic(ListView):
    model = Statistics
    context_object_name = 'statistics'
    template_name = 'influencers_statistic/statistics.html'
    extra_context = {'title': 'STATISTICS'}


    def get_queryset(self):
        username = self.kwargs.get('name')
        if username:
            return Statistics.objects.filter(username=username)
        return Statistics.objects.all()




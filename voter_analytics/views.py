from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Voter
from django.utils import timezone
from django.db.models import Q
import plotly.express as px
import plotly.io as pio

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  # Show 100 records per page

    def get_queryset(self):
        queryset = Voter.objects.all()
        
        # Retrieve filter parameters from GET request
        party_affiliation = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        voted_in_elections = self.request.GET.getlist('voted_in_elections')

        # Apply filters based on parameters
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)
        
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_year)
        
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_year)
        
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        
        if voted_in_elections:
            election_filters = Q()
            for election in voted_in_elections:
                election_filters |= Q(**{election: True})
            queryset = queryset.filter(election_filters)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add a list of years from 1920 to the current year
        current_year = timezone.now().year
        context['years'] = list(range(1860, current_year + 1))
        
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
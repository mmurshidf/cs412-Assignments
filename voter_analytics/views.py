# File: views.py
# Author: Mohammed Murshid (murshidm@bu.edu), 11/11/2024
# Description: Creates views for site

from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Voter
from django.utils import timezone
from django.db.models import Q
import plotly.express as px
from plotly.io import to_html
from datetime import datetime

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

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

class GraphOverviewView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voter_data'
    
    def get_queryset(self):
        queryset = Voter.objects.all()

        # Extract filter parameters from GET request
        selected_party = self.request.GET.get('party_affiliation')
        start_dob = self.request.GET.get('min_dob')
        end_dob = self.request.GET.get('max_dob')
        score_filter = self.request.GET.get('voter_score')
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        # Apply filters
        if selected_party:
            queryset = queryset.filter(party_affiliation=selected_party.strip())
        if start_dob:
            queryset = queryset.filter(date_of_birth__year__gte=int(start_dob))
        if end_dob:
            queryset = queryset.filter(date_of_birth__year__lte=int(end_dob))
        if score_filter:
            queryset = queryset.filter(voter_score=int(score_filter))
        for election in election_fields:
            if self.request.GET.get(election):
                queryset = queryset.filter(**{election: True})

        # Remove duplicates based on unique identifying characteristics
        unique_records = {}
        filtered_voters = []
        for record in queryset:
            identifier = (record.first_name, record.last_name, record.date_of_birth, record.party_affiliation)
            if identifier not in unique_records:
                unique_records[identifier] = True
                filtered_voters.append(record)

        return filtered_voters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the filtered voter data
        voters = self.get_queryset()

        # 1. Year of Birth Distribution Chart
        birth_year_list = [voter.date_of_birth.year for voter in voters]
        birth_year_chart = px.histogram(
            x=birth_year_list,
            nbins=100,
            title="Distribution of Voters by Year of Birth",
            labels={'x': 'Year of Birth', 'y': 'Number of Voters'}
        )
        context['year_of_birth_histogram'] = to_html(birth_year_chart, full_html=False)

        # 2. Party Affiliation Pie Chart
        party_counts_dict = {}
        for voter in voters:
            affiliation = voter.party_affiliation
            party_counts_dict[affiliation] = party_counts_dict.get(affiliation, 0) + 1
        party_pie_chart = px.pie(
            names=list(party_counts_dict.keys()),
            values=list(party_counts_dict.values()),
            title="Distribution of Voters by Party Affiliation",
            labels={'names': 'Party', 'values': 'Count'}
        )
        context['party_affiliation_pie'] = to_html(party_pie_chart, full_html=False)

        # 3. Election Participation Bar Chart
        participation_summary = {
            '2020 State': sum(voter.v20state for voter in voters),
            '2021 Town': sum(voter.v21town for voter in voters),
            '2021 Primary': sum(voter.v21primary for voter in voters),
            '2022 General': sum(voter.v22general for voter in voters),
            '2023 Town': sum(voter.v23town for voter in voters),
        }
        election_bar_chart = px.bar(
            x=list(participation_summary.keys()),
            y=list(participation_summary.values()),
            title="Voter Participation by Election",
            labels={'x': 'Election', 'y': 'Number of Voters'}
        )
        context['election_participation_bar'] = to_html(election_bar_chart, full_html=False)

        # Filter options to the context for the form
        context['party_options'] = Voter.objects.values_list('party_affiliation', flat=True).distinct()
        context['year_range'] = range(1900, datetime.now().year + 1)
        context['score_options'] = Voter.objects.values_list('voter_score', flat=True).distinct()
        context['election_fields'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        
        return context
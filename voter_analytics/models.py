# File: models.py
# Author: Mohammed Murshid (murshidm@bu.edu), 11/11/2024
# Description: Models file

from django.db import models
from datetime import datetime
import pandas as pd
# Create your models here.

class Voter(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Party: {self.party_affiliation}, Precinct: {self.precinct_number}, Score: {self.voter_score}"
    
    def load_data():
        data = pd.read_csv('newton_voters.csv')
        data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        for _, row in data.iterrows():
            Voter.objects.create(
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=str(row['Residential Address - Street Number']),
                street_name=row['Residential Address - Street Name'],
                apartment_number=row['Residential Address - Apartment Number'] or None,
                zip_code=str(row['Residential Address - Zip Code']),
                date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                party_affiliation=row['Party Affiliation'],
                precinct_number=row['Precinct Number'],
                v20state=bool(row['v20state']),
                v21town=bool(row['v21town']),
                v21primary=bool(row['v21primary']),
                v22general=bool(row['v22general']),
                v23town=bool(row['v23town']),
                voter_score=int(row['voter_score'])
            )
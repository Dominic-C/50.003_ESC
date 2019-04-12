from rest_framework import serializers
from .models import Preferences

class PreferencesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Preferences
		fields = ('first_name', 'last_name', 'subject_code', 'subject_name', 'cohort_size', 'cohort_num')
		




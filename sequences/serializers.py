from rest_framework import serializers
from .models import Genome, Gene, Variant

class GenomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genome
        fields = '__all__'

class GeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'
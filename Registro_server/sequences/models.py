from django.db import models

class Genome(models.Model):
    name = models.CharField(max_length=100)
    assembly_version = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Gene(models.Model):
    genome = models.ForeignKey(Genome, related_name='genes', on_delete=models.CASCADE)
    gene_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    start_position = models.IntegerField()
    end_position = models.IntegerField()

    def __str__(self):
        return self.name

class Variant(models.Model):
    gene = models.ForeignKey(Gene, related_name='variants', on_delete=models.CASCADE)
    variant_id = models.CharField(max_length=50)
    change = models.CharField(max_length=100)

    def __str__(self):
        return self.variant_id
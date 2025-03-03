# Generated by Django 5.1 on 2024-12-05 00:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genome",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("assembly_version", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Gene",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gene_id", models.CharField(max_length=50)),
                ("name", models.CharField(max_length=100)),
                ("start_position", models.IntegerField()),
                ("end_position", models.IntegerField()),
                (
                    "genome",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="genes",
                        to="sequences.genome",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Variant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("variant_id", models.CharField(max_length=50)),
                ("change", models.CharField(max_length=100)),
                (
                    "gene",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variants",
                        to="sequences.gene",
                    ),
                ),
            ],
        ),
    ]

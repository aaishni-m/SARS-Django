# Generated by Django 5.2.1 on 2025-05-17 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='body_pain',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='diarrhea',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='difficulty_breathing',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='dry_cough',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='fever',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patient',
            name='nasal_congestion',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='no_other_symptoms',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='runny_nose',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='severity',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Mild'), (2, 'Moderate'), (3, 'Severe')]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='sore_throat',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='patient',
            name='tiredness',
            field=models.BooleanField(),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-29 15:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aziende', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsertionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Insertion Type',
                'verbose_name_plural': 'Insertions Type',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Job Type',
                'verbose_name_plural': 'Jobs Type',
            },
        ),
        migrations.CreateModel(
            name='ProtectedCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Protected Category',
                'verbose_name_plural': 'Protected Categories',
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Qualification',
                'verbose_name_plural': 'Qualifications',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insertion_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Insertion Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('insertion_start_date', models.DateField(verbose_name='Insertion Start Date')),
                ('job_specifications', models.TextField(verbose_name='Job Specifications')),
                ('positions_required', models.IntegerField(verbose_name='Number of Positions Required')),
                ('insertion_duration', models.CharField(max_length=255, verbose_name='Insertion Duration')),
                ('insertion_finalization', models.BooleanField(verbose_name='Insertion Finalization')),
                ('transfer_available', models.BooleanField(verbose_name='Transfer Available')),
                ('incentives', models.TextField(verbose_name='Incentives')),
                ('car_available', models.BooleanField(verbose_name='Car Available')),
                ('previous_experience', models.BooleanField(verbose_name='Previous Experience')),
                ('experience_years', models.IntegerField(verbose_name='Experience Years')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aziende.company')),
                ('company_representative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aziende.companyrepresentative')),
                ('insertion_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancies.insertiontype', verbose_name='Insertion Type')),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancies.jobtype', verbose_name='Job Type')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aziende.office')),
                ('protected_category', models.ManyToManyField(to='vacancies.protectedcategory', verbose_name='Protected Category')),
                ('qualification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancies.qualification')),
            ],
            options={
                'verbose_name': 'Vacancy',
                'verbose_name_plural': 'Vacancies',
            },
        ),
        migrations.CreateModel(
            name='VacancyFileType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50, unique=True, verbose_name='Type')),
                ('descrizione', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Vacancy File Type',
                'verbose_name_plural': 'Vacancy File Types',
            },
        ),
        migrations.CreateModel(
            name='VacancyFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='vacancy/', verbose_name='File')),
                ('descrizione', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('tipo_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vacancy_files', to='vacancies.vacancyfiletype', verbose_name='File Type')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='vacancies.vacancy', verbose_name='Vacancy Files')),
            ],
        ),
    ]

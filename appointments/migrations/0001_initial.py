# Generated by Django 5.0.2 on 2024-02-27 04:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctors', '0003_alter_doctor_options_doctoravailability'),
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_and_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=20)),
                ('additional_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_patient', to='doctors.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments_as_doctor', to='patients.patient')),
            ],
            options={
                'verbose_name': 'appointment',
                'verbose_name_plural': 'appointments',
                'ordering': ['date_and_time'],
            },
        ),
    ]

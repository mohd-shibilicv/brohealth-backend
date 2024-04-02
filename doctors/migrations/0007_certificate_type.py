# Generated by Django 5.0.2 on 2024-03-30 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0006_remove_doctor_consultation_fee"),
    ]

    operations = [
        migrations.AddField(
            model_name="certificate",
            name="type",
            field=models.CharField(
                choices=[("image", "image"), ("pdf", "pdf")],
                default="image",
                max_length=20,
            ),
        ),
    ]
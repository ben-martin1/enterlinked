# Generated by Django 4.2.4 on 2023-09-05 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_company_ein_representative_line_of_business_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_address',
            field=models.TextField(max_length=319, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
# Generated by Django 4.2.4 on 2023-09-08 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('audition', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='rate',
        ),
        migrations.AddField(
            model_name='role',
            name='gender',
            field=models.CharField(choices=[('MAS', 'Cis Male'), ('FEM', 'Cis Female'), ('NBI', 'Non-Binary'), ('TFE', 'Transgender Female'), ('TMA', 'Transgender Male'), ('GNL', 'Gender Not Listed')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='role',
            name='sexual_orientation',
            field=models.CharField(choices=[('STR', 'STR'), ('GAY', 'GAY'), ('LES', 'LES'), ('BIS', 'BIS'), ('ONL', 'ONL')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='breakdown',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='audition.project'),
        ),
    ]

# Generated by Django 2.2.5 on 2019-10-02 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prescription_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kcdCode', models.CharField(max_length=8)),
                ('diesName', models.CharField(max_length=255)),
                ('rgstrDate', models.DateTimeField(auto_now_add=True)),
                ('linkPrescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prescription_manage.Prescription')),
            ],
        ),
    ]

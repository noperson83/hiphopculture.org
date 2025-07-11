# Generated by Django 2.2.3 on 2019-08-11 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a device manufacturer', max_length=40)),
                ('google_maps_link', models.CharField(blank=True, help_text='Google map link', max_length=200, null=True)),
                ('manu_address', models.CharField(blank=True, default='1234 N Strong. Dr', help_text='Manufacturer address', max_length=100)),
                ('manu_address_city', models.CharField(blank=True, help_text='Manufacturer city', max_length=100)),
                ('manu_address_state', models.CharField(blank=True, help_text='Manufacturer state', max_length=100)),
                ('manu_address_zipcode', models.CharField(blank=True, help_text='Manufacturer zip', max_length=100)),
                ('dateofcreation', models.DateTimeField(auto_now_add=True, help_text='Created at', null=True)),
                ('lastmodification', models.DateTimeField(auto_now=True, help_text='Last modified', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a Distributor name.', max_length=40)),
                ('google_maps_link', models.CharField(blank=True, help_text='Google map link', max_length=200, null=True)),
                ('billing_address', models.CharField(blank=True, default='1234 N Strong. Dr', help_text='Distributor address', max_length=100)),
                ('billing_address_city', models.CharField(blank=True, help_text='Distributor city', max_length=100)),
                ('billing_address_state', models.CharField(blank=True, help_text='Distributor state', max_length=100)),
                ('billing_address_zipcode', models.CharField(blank=True, help_text='Distributor zip', max_length=100)),
                ('dateofcreation', models.DateTimeField(auto_now_add=True, help_text='Created at', null=True)),
                ('lastmodification', models.DateTimeField(auto_now=True, help_text='Last modified', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the software manufacturer', max_length=60)),
                ('dateofcreation', models.DateTimeField(auto_now_add=True, help_text='Created at', null=True)),
                ('lastmodification', models.DateTimeField(auto_now=True, help_text='Last modified', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WireManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a Manufacturer name.', max_length=40)),
                ('dateofcreation', models.DateTimeField(auto_now_add=True, help_text='Created at', null=True)),
                ('lastmodification', models.DateTimeField(auto_now=True, help_text='Last modified', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WireMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_num', models.CharField(blank=True, help_text='Enter a part number.', max_length=60)),
                ('general_disc', models.CharField(help_text='Enter a general description.', max_length=200)),
                ('part_disc', models.CharField(blank=True, help_text='Enter part description.', max_length=200)),
                ('cost', models.DecimalField(decimal_places=2, default='0.60', help_text='Cost', max_digits=18)),
                ('msrp', models.DecimalField(decimal_places=2, default='1.00', help_text='MSRP', max_digits=18)),
                ('dateofcreation', models.DateTimeField(auto_now_add=True, help_text='Created at', null=True)),
                ('lastmodification', models.DateTimeField(auto_now=True, help_text='Last modified', null=True)),
                ('dist', models.ForeignKey(help_text='distributor', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wdistributor', related_query_name='wdistributor', to='material.Distributor')),
                ('wmfg', models.ForeignKey(help_text='wManufacturer', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wmanufacturer', related_query_name='wmanufacturer', to='material.WireManufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_num', models.CharField(blank=True, help_text='Enter a part number.', max_length=60)),
                ('general_disc', models.CharField(help_text='Enter a general description.', max_length=200)),
                ('part_disc', models.CharField(blank=True, help_text='Enter part description.', max_length=200)),
                ('cost', models.DecimalField(decimal_places=2, default='0.65', help_text='Cost', max_digits=18)),
                ('msrp', models.DecimalField(decimal_places=2, default='1.00', help_text='MSRP', max_digits=18)),
                ('dateofcreation', models.DateTimeField(auto_now_add=True, help_text='Created at', null=True)),
                ('lastmodification', models.DateTimeField(auto_now=True, help_text='Last modified', null=True)),
                ('dist', models.ForeignKey(help_text='sistributor', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sdistributor', related_query_name='sdistributor', to='material.Distributor')),
                ('smfg', models.ForeignKey(help_text='dSoftware', null=True, on_delete=django.db.models.deletion.SET_NULL, to='material.SoftwareManufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='HardwareMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hmfg', models.CharField(help_text='Enter a manufacturer.', max_length=60, unique=True)),
                ('part_num', models.CharField(blank=True, help_text='Enter a model number.', max_length=60)),
                ('general_disc', models.CharField(help_text='Enter a general description.', max_length=200)),
                ('dateofcreation', models.DateTimeField(auto_now_add=True, help_text='Created at', null=True)),
                ('lastmodification', models.DateTimeField(auto_now=True, help_text='Last modified', null=True)),
                ('dist', models.ForeignKey(help_text='distributor', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hdistributor', related_query_name='hdistributor', to='material.Distributor')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_num', models.CharField(blank=True, help_text='Enter a part number.', max_length=60)),
                ('general_disc', models.CharField(help_text='Enter a general description.', max_length=200)),
                ('part_disc', models.CharField(blank=True, help_text='Enter part description.', max_length=200)),
                ('cost', models.DecimalField(decimal_places=2, default='0.65', help_text='Cost', max_digits=18)),
                ('msrp', models.DecimalField(decimal_places=2, default='1.00', help_text='MSRP', max_digits=18)),
                ('dateofcreation', models.DateTimeField(auto_now_add=True, help_text='Created at', null=True)),
                ('lastmodification', models.DateTimeField(auto_now=True, help_text='Last modified', null=True)),
                ('dist', models.ForeignKey(help_text='distributor', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ddistributor', related_query_name='ddistributor', to='material.Distributor')),
                ('dmfg', models.ForeignKey(help_text='dManufacturer', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dmanufacturer', related_query_name='dmanufacturer', to='material.DeviceManufacturer')),
            ],
        ),
    ]

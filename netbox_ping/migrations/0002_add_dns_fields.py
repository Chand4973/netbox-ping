from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('netbox_ping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pluginsettingsmodel',
            name='dns_server1',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=255,
                verbose_name='Primary DNS Server',
                help_text='Primary DNS server (e.g., 8.8.8.8)'
            ),
        ),
        migrations.AddField(
            model_name='pluginsettingsmodel',
            name='dns_server2',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=255,
                verbose_name='Secondary DNS Server',
                help_text='Secondary DNS server (e.g., 8.8.4.4)'
            ),
        ),
        migrations.AddField(
            model_name='pluginsettingsmodel',
            name='dns_server3',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=255,
                verbose_name='Tertiary DNS Server',
                help_text='Tertiary DNS server'
            ),
        ),
        migrations.AddField(
            model_name='pluginsettingsmodel',
            name='perform_dns_lookup',
            field=models.BooleanField(
                default=True,
                verbose_name='Perform DNS Lookups',
                help_text='Whether to perform DNS lookups when scanning IPs'
            ),
        ),
    ] 
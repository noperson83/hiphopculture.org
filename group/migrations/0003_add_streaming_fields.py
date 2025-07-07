from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_auto_20250226_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='youtube_url',
            field=models.URLField(blank=True, help_text='YouTube channel URL', max_length=200),
        ),
        migrations.AddField(
            model_name='group',
            name='spotify_url',
            field=models.URLField(blank=True, help_text='Spotify profile URL', max_length=200),
        ),
        migrations.AddField(
            model_name='group',
            name='apple_music_url',
            field=models.URLField(blank=True, help_text='Apple Music profile URL', max_length=200),
        ),
        migrations.AddField(
            model_name='group',
            name='soundcloud_url',
            field=models.URLField(blank=True, help_text='SoundCloud profile URL', max_length=200),
        ),
        migrations.AddField(
            model_name='group',
            name='bandcamp_url',
            field=models.URLField(blank=True, help_text='Bandcamp profile URL', max_length=200),
        ),
        migrations.AddField(
            model_name='group',
            name='tidal_url',
            field=models.URLField(blank=True, help_text='Tidal profile URL', max_length=200),
        ),
        migrations.AddField(
            model_name='group',
            name='shazam_url',
            field=models.URLField(blank=True, help_text='Shazam profile URL', max_length=200),
        ),
        migrations.AddField(
            model_name='group',
            name='tiktok_url',
            field=models.URLField(blank=True, help_text='TikTok profile URL', max_length=200),
        ),
    ]

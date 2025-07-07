from django.db import migrations, models
import group.models

class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_add_streaming_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='background_image',
            field=models.ImageField(blank=True, default='home/images/LMNlogo.jpg', help_text='Background image', max_length=60, null=True, upload_to=group.models.upload_to_group_folder),
        ),
    ]

from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_alter_usuario_token_recuperacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='token_recuperacion_fecha',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
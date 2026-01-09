from django.db import migrations


def create_initial_topics(apps, schema_editor):
    Topic = apps.get_model("topics", "Topic")
    Topic.objects.get_or_create(name="Python")
    Topic.objects.get_or_create(name="Django")
    Topic.objects.get_or_create(name="DevOps")


class Migration(migrations.Migration):

    dependencies = [
        ("topics", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_topics),
    ]

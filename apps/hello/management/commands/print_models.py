from django.core.management.base import BaseCommand
import django.db.models


class Command(BaseCommand):
    help = 'Prints all models and objects count in each of them'

    def handle(self, *args, **options):
        models = django.db.models.get_models()
        for model in models:
            obj_count = model.objects.count()
            out_str = "Model: {0}, objects count: {1}".\
                format(model._meta.model_name, obj_count)
            self.stdout.write(out_str)
            self.stderr.write('error: ' + out_str)

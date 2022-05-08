from django.db import transaction


@transaction.atomic
def bulk_save(items):
    for item in items:
        item.save()

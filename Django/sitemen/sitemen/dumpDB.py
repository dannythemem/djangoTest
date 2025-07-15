from django.core.management import call_command
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitemen.settings')
django.setup()
with open('../../../fixtures/data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'men.Category', 'men.Men', 'men.Wife', 'men.TagPost', stdout=f)
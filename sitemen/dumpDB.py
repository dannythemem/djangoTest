from django.core.serializers import serialize
import os, django, json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sitemen.settings")
django.setup()
from men.models import Men

# Загружаем уже существующий data.json
with open('../fixtures/data.json', encoding='utf-8') as f:
    existing_data = json.load(f)

# Получаем новую запись как Python-объект
new_data_raw = serialize('json', Men.objects.filter(pk=7), indent=4)
new_data = json.loads(new_data_raw)

# Объединяем
combined_data = existing_data + new_data

# Перезаписываем data.json (один валидный массив)
with open('../fixtures/data.json', 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, indent=4, ensure_ascii=False)

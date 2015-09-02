import json


def convert_to_json(form):
    if form.is_valid():
        json_ctx = dict({'ok': True})
    else:
        json_ctx = dict({'ok': False})
        json_ctx['errors'] = form.errors
    return json.dumps(json_ctx, encoding='utf-8', ensure_ascii=False)

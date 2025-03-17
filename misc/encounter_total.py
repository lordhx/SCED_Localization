import json

campaign_filename = 'repos/arkhamdb-json-data/pack/fhv/fhvc.json'
with open(campaign_filename, 'r', encoding='utf-8') as object_file:
    totals = {}
    for card in json.loads(object_file.read()):
        totals[card['encounter_code']] = totals.get(card['encounter_code'], 0) + card['quantity']

    print(totals)
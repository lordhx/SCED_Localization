def transform_taboo():
    return 'Табу'

def transform_vengeance(vengeance):
    return vengeance.replace('Vengeance', 'Возмездие')

def transform_victory(victory):
    return victory.replace('Victory', 'Победа')

def transform_shelter(shelter):
    return shelter.replace('Shelter', 'Убежище')

def transform_blob(blob):
    return blob.replace('Blob', 'Сгусток')

def transform_tracker(tracker):
    if tracker == 'Current Depth':
        return 'Текущая Глубина'
    elif tracker == 'Spent Keys':
        return 'Потраченные Ключи'
    elif tracker == 'Strength of the Abyss':
        return 'Сила Бездны'
    return tracker


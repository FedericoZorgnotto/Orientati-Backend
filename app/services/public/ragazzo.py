def ragazzi_from_genitore(genitore):
    """
    Restituisce i ragazzi associati a un genitore
    """
    ragazzi = []
    for ragazzo in genitore.ragazzi:
        ragazzi.append(ragazzo)
    return ragazzi

import re

from sqlalchemy import select

from ExploData.explo_data.bio_data.genus import data as bio_genus
from ExploData.explo_data.db import CodexScans

from ExploData.explo_data import db

from bio_scan.bio_data.species import rules as bio_types
from bio_scan.util import translate_species


def check_codex(commander: int, region: int | None, genus: str, species: str, variant: str = '') -> bool:
    if genus not in bio_genus:
        return False
    biological = species
    if variant:
        if species in bio_genus:
            code = ''
            color_data = bio_genus[species]['colors']['star']
            for key, color in color_data.items():  # type: str, str
                if color == variant:
                    code = key.capitalize()
                    break
            if code:
                match = re.match('^(.*)_Name;$', species)
                if match:
                    biological = f'{match.group(1)}_{code}_Name;'

        elif 'colors' in bio_genus[genus]:
            variant_data = bio_genus[genus]['colors']
            code = ''
            color_data = []
            if 'species' in variant_data:
                if 'star' in variant_data['species'][species]:
                    color_data = variant_data['species'][species]['star']
                elif 'element' in variant_data['species'][species]:
                    color_data = variant_data['species'][species]['element']
            else:
                color_data = variant_data['star']
            for key, color in color_data.items():  # type: str, str
                if color == variant:
                    code = key.capitalize()
                    break

            if code:
                match = re.match('^(.*)_Name;$', species)
                if match:
                    biological = f'{match.group(1)}_{code}_Name;'

    session = db.get_session()

    if region is not None:
        entry: CodexScans = session.scalar(select(CodexScans).where(CodexScans.commander_id == commander)
                                           .where(CodexScans.region == region).where(CodexScans.biological == biological))
    else:
        entry: CodexScans = session.scalar(select(CodexScans).where(CodexScans.commander_id == commander)
                                           .where(CodexScans.biological == biological))

    session.close()

    if entry:
        return True
    return False


def check_codex_from_name(commander: int, region: int | None, name: str, variant: str = '') -> bool:
    for genus, species_data in bio_types.items():
        for species_code, data in species_data.items():
            if translate_species(data['name']) == name:
                return check_codex(commander, region, genus, species_code, variant)
    return False

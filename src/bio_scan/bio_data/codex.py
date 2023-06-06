import re

from sqlalchemy import select
from sqlalchemy.orm import scoped_session

from bio_scan.bio_data.genus import data as bio_genus
from bio_scan.bio_data.species import rules as bio_types
from bio_scan.body_data.db import CodexScans

bio_codex_map = {
    '$Codex_Ent_Aleoids_Genus_Name;': {
        '$Codex_Ent_Aleoids_01_',
        '$Codex_Ent_Aleoids_02_',
        '$Codex_Ent_Aleoids_03_',
        '$Codex_Ent_Aleoids_04_',
        '$Codex_Ent_Aleoids_05_',
    },
    '$Codex_Ent_Bacterial_Genus_Name;': {
        '$Codex_Ent_Bacterial_01_',
        '$Codex_Ent_Bacterial_02_',
        '$Codex_Ent_Bacterial_03_',
        '$Codex_Ent_Bacterial_04_',
        '$Codex_Ent_Bacterial_05_',
        '$Codex_Ent_Bacterial_06_',
        '$Codex_Ent_Bacterial_07_',
        '$Codex_Ent_Bacterial_08_',
        '$Codex_Ent_Bacterial_09_',
        '$Codex_Ent_Bacterial_10_',
        '$Codex_Ent_Bacterial_11_',
        '$Codex_Ent_Bacterial_12_',
        '$Codex_Ent_Bacterial_13_',
    },
    '$Codex_Ent_Cactoid_Genus_Name;': {
        '$Codex_Ent_Cactoid_01_',
        '$Codex_Ent_Cactoid_02_',
        '$Codex_Ent_Cactoid_03_',
        '$Codex_Ent_Cactoid_04_',
        '$Codex_Ent_Cactoid_05_',
    },
    '$Codex_Ent_Clypeus_Genus_Name;': {
        '$Codex_Ent_Clypeus_01_',
        '$Codex_Ent_Clypeus_02_',
        '$Codex_Ent_Clypeus_03_',
    },
    '$Codex_Ent_Conchas_Genus_Name;': {
        '$Codex_Ent_Conchas_01_',
        '$Codex_Ent_Conchas_02_',
        '$Codex_Ent_Conchas_03_',
        '$Codex_Ent_Conchas_04_',
    },
    '$Codex_Ent_Cone_Name;': {  # No atmos, near center of nebula
        '$Codex_Ent_Cone_'
    },
    '$Codex_Ent_Electricae_Genus_Name;': {
        '$Codex_Ent_Electricae_01_',
        '$Codex_Ent_Electricae_02_',
    },
    '$Codex_Ent_Fonticulus_Genus_Name;': {
        '$Codex_Ent_Fonticulus_01_',
        '$Codex_Ent_Fonticulus_02_',
        '$Codex_Ent_Fonticulus_03_',
        '$Codex_Ent_Fonticulus_04_',
        '$Codex_Ent_Fonticulus_05_',
        '$Codex_Ent_Fonticulus_06_',
    },
    '$Codex_Ent_Fumerolas_Genus_Name;': {
        '$Codex_Ent_Fumerolas_01_',
        '$Codex_Ent_Fumerolas_02_',
        '$Codex_Ent_Fumerolas_03_',
        '$Codex_Ent_Fumerolas_04_',
    },
    '$Codex_Ent_Fungoids_Genus_Name;': {
        '$Codex_Ent_Fungoids_01_',
        '$Codex_Ent_Fungoids_02_',
        '$Codex_Ent_Fungoids_03_',
        '$Codex_Ent_Fungoids_04_',
    },
    '$Codex_Ent_Ground_Struct_Ice_Name;': {
        '$Codex_Ent_Ground_Struct_Ice_'
    },
    '$Codex_Ent_Osseus_Genus_Name;': {
        '$Codex_Ent_Osseus_01_',
        '$Codex_Ent_Osseus_02_',
        '$Codex_Ent_Osseus_03_',
        '$Codex_Ent_Osseus_04_',
        '$Codex_Ent_Osseus_05_',
        '$Codex_Ent_Osseus_06_',
    },
    '$Codex_Ent_Recepta_Genus_Name;': {
        '$Codex_Ent_Recepta_01_',
        '$Codex_Ent_Recepta_02_',
        '$Codex_Ent_Recepta_03_',
    },
    '$Codex_Ent_Brancae_Name;': {
        '$Codex_Ent_Seed_',
        '$Codex_Ent_SeedABCD_01_',
        '$Codex_Ent_SeedABCD_02_',
        '$Codex_Ent_SeedABCD_03_',
        '$Codex_Ent_SeedEFGH_01_',
        '$Codex_Ent_SeedEFGH_02_',
        '$Codex_Ent_SeedEFGH_03_',
        '$Codex_Ent_SeedEFGH_',
    },
    '$Codex_Ent_Shrubs_Genus_Name;': {
        '$Codex_Ent_Shrubs_01_',
        '$Codex_Ent_Shrubs_02_',
        '$Codex_Ent_Shrubs_03_',
        '$Codex_Ent_Shrubs_04_',
        '$Codex_Ent_Shrubs_05_',
        '$Codex_Ent_Shrubs_06_',
        '$Codex_Ent_Shrubs_07_',
    },
    '$Codex_Ent_Sphere_Name;': {
        '$Codex_Ent_Sphere_',
        '$Codex_Ent_SphereABCD_01_',
        '$Codex_Ent_SphereABCD_02_',
        '$Codex_Ent_SphereABCD_03_',
        '$Codex_Ent_SphereEFGH_01_',
        '$Codex_Ent_SphereEFGH_02_',
        '$Codex_Ent_SphereEFGH_03_',
        '$Codex_Ent_SphereEFGH_',
    },
    '$Codex_Ent_Stratum_Genus_Name;': {
        '$Codex_Ent_Stratum_01_',
        '$Codex_Ent_Stratum_02_',
        '$Codex_Ent_Stratum_03_',
        '$Codex_Ent_Stratum_04_',
        '$Codex_Ent_Stratum_05_',
        '$Codex_Ent_Stratum_06_',
        '$Codex_Ent_Stratum_07_',
        '$Codex_Ent_Stratum_08_',
    },
    '$Codex_Ent_Tube_Name;': {
        '$Codex_Ent_Tube_',
        '$Codex_Ent_TubeABCD_01_',
        '$Codex_Ent_TubeABCD_02_',
        '$Codex_Ent_TubeABCD_03_',
        '$Codex_Ent_TubeEFGH_01_',
        '$Codex_Ent_TubeEFGH_02_',
        '$Codex_Ent_TubeEFGH_03_',
        '$Codex_Ent_TubeEFGH_',
    },
    '$Codex_Ent_Tubus_Genus_Name;': {
        '$Codex_Ent_Tubus_01_',
        '$Codex_Ent_Tubus_02_',
        '$Codex_Ent_Tubus_03_',
        '$Codex_Ent_Tubus_04_',
        '$Codex_Ent_Tubus_05_',
    },
    '$Codex_Ent_Tussocks_Genus_Name;': {
        '$Codex_Ent_Tussocks_01_',
        '$Codex_Ent_Tussocks_02_',
        '$Codex_Ent_Tussocks_03_',
        '$Codex_Ent_Tussocks_04_',
        '$Codex_Ent_Tussocks_05_',
        '$Codex_Ent_Tussocks_06_',
        '$Codex_Ent_Tussocks_07_',
        '$Codex_Ent_Tussocks_08_',
        '$Codex_Ent_Tussocks_09_',
        '$Codex_Ent_Tussocks_10_',
        '$Codex_Ent_Tussocks_11_',
        '$Codex_Ent_Tussocks_12_',
        '$Codex_Ent_Tussocks_13_',
        '$Codex_Ent_Tussocks_14_',
        '$Codex_Ent_Tussocks_15_',
    },
    '$Codex_Ent_Vents_Name;': {
        '$Codex_Ent_Vents_',
    },
}

bio_color_suffix_map = {
    'O': 'star',
    'B': 'star',
    'A': 'star',
    'F': 'star',
    'G': 'star',
    'K': 'star',
    'M': 'star',
    'L': 'star',
    'T': 'star',
    'TTS': 'star',
    'Y': 'star',
    'W': 'star',
    'D': 'star',
    'N': 'star',
    'H': 'star',
    'Antimony': 'element',
    'Polonium': 'element',
    'Ruthenium': 'element',
    'Technetium': 'element',
    'Tellurium': 'element',
    'Yttrium': 'element',
    'Cadmium': 'element',
    'Mercury': 'element',
    'Molybdenum': 'element',
    'Niobium': 'element',
    'Tungsten': 'element',
    'Tin': 'element'
}


def parse_variant(name: str) -> tuple[str, str, str]:
    for genus, search_set in bio_codex_map.items():
        for search in search_set:
            if name.startswith(search):
                for species in bio_types[genus]:
                    if species.startswith(search):
                        color_type = name.split(search)[1].split('_Name')[0]
                        color = ''
                        if color_type in bio_color_suffix_map:
                            match bio_color_suffix_map[color_type]:
                                case 'star':
                                    try:
                                        color = bio_genus[genus]['colors']['species'][species]['star'][color_type]
                                    except KeyError:
                                        try:
                                            color = bio_genus[genus]['colors']['star'][color_type]
                                        except KeyError:
                                            color = ''
                                case 'element':
                                    try:
                                        color = bio_genus[genus]['colors']['species'][species]['element'][color_type.lower()]
                                    except KeyError:
                                        color = ''

                        return genus, species, color
    return '', '', ''


def set_codex(session_factory: scoped_session, commander: int, biological: str, region: int) -> None:
    if region is None:
        return

    session = session_factory()
    entry: CodexScans = session.scalar(select(CodexScans).where(CodexScans.commander_id == commander)
                                       .where(CodexScans.biological == biological).where(CodexScans.region == region))
    if not entry:
        entry = CodexScans(commander_id=commander, biological=biological, region=region)
        session.add(entry)
        session.commit()
    session.close()


def check_codex(session_factory: scoped_session, commander: int, region: int, genus: str, species: str, variant: str = '') -> bool:
    biological = species
    if variant:
        if 'colors' in bio_genus[genus]:
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

    session = session_factory()
    entry: CodexScans = session.scalar(select(CodexScans).where(CodexScans.commander_id == commander)
                                       .where(CodexScans.region == region).where(CodexScans.biological == biological))
    session.close()

    if entry:
        return True
    return False

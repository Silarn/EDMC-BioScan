from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Brancae_Name;': {
        '$Codex_Ent_Seed_Name;': {
            'name': 'Roseum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': 'Any',
                    'guardian': True,
                    'region': ['brain-tree']
                }
            ],
        },
        '$Codex_Ent_SeedABCD_01_Name;': {
            'name': 'Gypseeum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'body_type': ['Rocky body'],
                    'min_temperature': 200.0,
                    'max_temperature': 400.0,
                    'max_gravity': 0.42,
                    'volcanism': ['metallic', 'rocky', 'silicate', 'water'],
                    'guardian': True,
                    'region': ['brain-tree'],
                    'bodies': ['Earthlike body', 'Gas giant with water based life', 'Water giant']
                }
            ],
        },
        '$Codex_Ent_SeedABCD_02_Name;': {
            'name': 'Ostrinum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'body_type': ['Metal rich body', 'Rocky body', 'High metal content body'],
                    'volcanism': ['metallic', 'rocky', 'silicate'],
                    'guardian': True,
                    'region': ['brain-tree']
                }
            ],
        },
        '$Codex_Ent_SeedABCD_03_Name;': {
            'name': 'Viride Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'body_type': ['Rocky ice body'],
                    'min_temperature': 100.0,
                    'max_temperature': 270.0,
                    'max_gravity': 0.4,
                    'volcanism': 'Any',
                    'guardian': True,
                    'region': ['brain-tree'],
                    'bodies': ['Earthlike body', 'Gas giant with water based life', 'Water giant']
                }
            ],
        },
        '$Codex_Ent_SeedEFGH_01_Name;': {
            'name': 'Aureum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'min_temperature': 300.0,
                    'max_temperature': 500.0,
                    'max_gravity': 2.9,
                    'volcanism': ['metallic', 'rocky', 'silicate'],
                    'guardian': True,
                    'region': ['brain-tree'],
                    #'bodies': ['Earthlike body', 'Gas giant with water based life', 'Water giant']
                }
            ],
        },
        '$Codex_Ent_SeedEFGH_02_Name;': {
            'name': 'Puniceum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'volcanism': 'Any',
                    'guardian': True,
                    'region': ['brain-tree'],
                    'bodies': ['Earthlike body', 'Gas giant with water based life', 'Water giant']
                }
            ],
        },
        '$Codex_Ent_SeedEFGH_03_Name;': {
            'name': 'Lindigoticum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_temperature': 300.0,
                    'max_temperature': 500.0,
                    'max_gravity': 2.7,
                    'volcanism': ['rocky', 'silicate', 'metallic'],
                    'guardian': True,
                    'region': ['brain-tree'],
                    'bodies': ['Earthlike body', 'Gas giant with water based life', 'Water giant']
                }
            ],
        },
        '$Codex_Ent_SeedEFGH_Name;': {
            'name': 'Lividum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'body_type': ['Rocky body'],
                    'min_temperature': 300.0,
                    'max_temperature': 500.0,
                    'max_gravity': 0.5,
                    'volcanism': ['metallic', 'rocky', 'silicate', 'water'],
                    'guardian': True,
                    'region': ['brain-tree'],
                    #'bodies': ['Earthlike body', 'Gas giant with water based life', 'Water giant']
                }
            ],
        },
    },
}

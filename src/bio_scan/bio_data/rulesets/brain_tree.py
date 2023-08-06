from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Brancae_Name;': {
        '$Codex_Ent_Seed_Name;': {
            'name': 'Roseum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'min_temperature': 200.0,
                    'max_temperature': 500.0,
                    'volcanism': 'Any',
                    'guardian': True
                }
            ],
        },
        '$Codex_Ent_SeedABCD_01_Name;': {
            'name': 'Gypseeum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'body_type': ['Rocky body'],
                    'min_temperature': 200.0,
                    'max_temperature': 330.0,
                    'volcanism': ['metallic', 'rocky', 'silicate', 'water'],
                    'life': True
                }
            ],
        },
        '$Codex_Ent_SeedABCD_02_Name;': {
            'name': 'Ostrinum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'min_temperature': 125.0,
                    'volcanism': ['metallic', 'rocky', 'silicate'],
                    'guardian': True,
                    'life': True
                }
            ],
        },
        '$Codex_Ent_SeedABCD_03_Name;': {
            'name': 'Viride Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'body_type': ['Rocky ice body'],
                    'min_temperature': 100.0,
                    'max_temperature': 270.0,
                    'volcanism': ['metallic', 'rocky', 'silicate', 'carbon dioxide', 'water'],
                    'guardian': True,
                    'life': True
                }
            ],
        },
        '$Codex_Ent_SeedEFGH_01_Name;': {
            'name': 'Aureum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'min_temperature': 300.0,
                    'max_temperature': 500.0,
                    'volcanism': ['metallic', 'rocky', 'silicate'],
                    'guardian': True,
                    'life': True
                }
            ],
        },
        '$Codex_Ent_SeedEFGH_02_Name;': {
            'name': 'Puniceum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'min_temperature': 125.0,
                    'volcanism': 'Any',
                    'guardian': True,
                    'life': True
                }
            ],
        },
        '$Codex_Ent_SeedEFGH_03_Name;': {
            'name': 'Lindigoticum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_temperature': 300.0,
                    'max_temperature': 500.0,
                    'volcanism': ['rocky', 'silicate', 'metallic'],
                    'guardian': True,
                    'life': True
                }
            ],
        },
        '$Codex_Ent_SeedEFGH_Name;': {
            'name': 'Lividum Brain Tree',
            'value': 1593700,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'body_type': ['Rocky body'],
                    'min_temperature': 300.0,
                    'max_temperature': 500.0,
                    'volcanism': ['metallic', 'rocky', 'silicate', 'water'],
                    'guardian': True,
                    'life': True
                }
            ],
        },
    },
}

from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Sphere_Name;': {
        '$Codex_Ent_Sphere_Name;': {
            'name': 'Luteolum Anemone',
            'value': 1499900,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'min_gravity': 0.044,
                    'max_gravity': 1.28,
                    'max_temperature': 440.0,
                    'min_temperature': 200.0,
                    'volcanism': ['metallic', 'silicate', 'rocky', 'water'],
                    'body_type': ['Rocky body'],
                    'main_star': [('B', 'IV'), ('B', 'V')]
                }
            ],
        },
        '$Codex_Ent_SphereABCD_01_Name;': {
            'name': 'Croceum Anemone',
            'value': 1499900,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'min_gravity': 0.047,
                    'max_gravity': 0.37,
                    'max_temperature': 440.0,
                    'min_temperature': 200.0,
                    'volcanism': ['silicate', 'rocky', 'metallic'],
                    'body_type': ['Rocky body'],
                    'main_star': [('B', 'V'), ('B', 'VI'), ('A', 'III')]
                }
            ],
        },
        '$Codex_Ent_SphereABCD_02_Name;': {
            'name': 'Puniceum Anemone',
            'value': 1499900,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'min_gravity': 0.17,
                    'max_gravity': 2.52,
                    'max_temperature': 800.0,
                    'min_temperature': 65.0,
                    'volcanism': 'None',
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'special': ['O', 'WC']
                },
                {
                    'atmosphere': ['None'],
                    'min_gravity': 0.17,
                    'max_gravity': 2.52,
                    'max_temperature': 800.0,
                    'min_temperature': 65.0,
                    'volcanism': ['carbon dioxide geysers'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'special': ['O', 'WC']
                }
            ],
        },
        '$Codex_Ent_SphereABCD_03_Name;': {
            'name': 'Roseum Anemone',
            'value': 1499900,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.37,
                    'max_temperature': 440.0,
                    'min_temperature': 200.0,
                    'volcanism': ['silicate', 'rocky', 'metallic'],
                    'body_type': ['Rocky body'],
                    'special': [('B', 'I'), ('B', 'II'), ('B', 'III'), ('B', 'IV')]
                }
            ],
        },
        '$Codex_Ent_SphereEFGH_01_Name;': {
            'name': 'Rubeum Bioluminescent Anemone',
            'value': 1499900,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'min_gravity': 0.036,
                    'max_gravity': 4.61,
                    'min_temperature': 160.0,
                    'max_temperature': 1800.0,
                    'volcanism': 'Any',
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'main_star': [('B', 'VI'), 'A', ('F', 'I'), ('F', 'II'), 'N', 'H', 'O']
                }
            ],
        },
        '$Codex_Ent_SphereEFGH_02_Name;': {
            'name': 'Prasinum Bioluminescent Anemone',
            'value': 1499900,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'min_gravity': 0.036,
                    'min_temperature': 110.0,
                    'max_temperature': 3050.0,
                    'volcanism': ['carbon dioxide'],
                    'body_type': ['Metal rich body', 'Rocky body', 'High metal content body'],
                    'main_star': ['O', ('B', 'IV'), ('B', 'V'), 'WC', 'WO', 'AeBe']
                },
                {
                    'atmosphere': ['None'],
                    'min_gravity': 0.036,
                    'min_temperature': 110.0,
                    'max_temperature': 3050.0,
                    'volcanism': 'None',
                    'body_type': ['Metal rich body', 'Rocky body', 'High metal content body'],
                    'main_star': ['O', ('B', 'IV'), ('B', 'V'), 'WC', 'WO', 'AeBe']
                }
            ],
        },
        '$Codex_Ent_SphereEFGH_03_Name;': {
            'name': 'Roseum Bioluminescent Anemone',
            'value': 1499900,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'min_gravity': 0.036,
                    'max_gravity': 4.61,
                    'min_temperature': 400.0,
                    'volcanism': 'Any',
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'special': ['B', ('A', 'II'), ('A', 'I'), 'H']
                }
            ],
        },
        '$Codex_Ent_SphereEFGH_Name;': {
            'name': 'Blatteum Bioluminescent Anemone',
            'value': 1499900,
            'rulesets': [
                {
                    'atmosphere': ['None'],
                    'min_temperature': 220.0,
                    'volcanism': 'Any',
                    'body_type': ['Metal rich body', 'High metal content body'],
                    'main_star': [('B', 'IV'), ('B', 'V'), 'H', 'N', 'O', ('K', 'III'), ('K', 'IV')]
                }
            ],
        },
    },
}

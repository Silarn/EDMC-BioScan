from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Fumerolas_Genus_Name;': {
        '$Codex_Ent_Fumerolas_01_Name;': {
            'name': 'Fumerola Carbosis',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': 'Any',
                    'max_gravity': 0.275,
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'volcanism': ['carbon', 'methane']
                }
            ],
        },
        '$Codex_Ent_Fumerolas_02_Name;': {
            'name': 'Fumerola Extremus',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': 'Any',
                    'max_gravity': 0.275,
                    'body_type': ['Rock body', 'Rocky ice body', 'High metal content body'],
                    'volcanism': ['silicate', 'iron', 'rocky']
                }
            ],
        },
        '$Codex_Ent_Fumerolas_03_Name;': {
            'name': 'Fumerola Nitris',
            'value': 7500900,
            'rulesets': [
                {
                    'atmosphere': 'Any',
                    'max_gravity': 0.275,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                }
            ],
        },
        '$Codex_Ent_Fumerolas_04_Name;': {
            'name': 'Fumerola Aquatis',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': 'Any',
                    'max_gravity': 0.275,
                    'body_type': ['Icy body', 'Rocky ice body', 'Rocky body'],
                    'volcanism': ['water']
                }
            ],
        },
    },
}

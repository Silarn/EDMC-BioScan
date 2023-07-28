from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Clypeus_Genus_Name;': {
        '$Codex_Ent_Clypeus_01_Name;': {
            'name': 'Clypeus Lacrimam',
            'value': 8418000,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 190.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.054,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.054,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.054,
                    'volcanism': ['water']
                }
            ],
        },
        '$Codex_Ent_Clypeus_02_Name;': {
            'name': 'Clypeus Margaritus',
            'value': 11873200,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 190.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.054,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.054,
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Clypeus_03_Name;': {
            'name': 'Clypeus Speculumi',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 190.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.055,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None',
                    'distance': 2000.0
                },
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.055,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None',
                    'distance': 2000.0
                },
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.055,
                    'body_type': ['Rocky body'],
                    'volcanism': ['water'],
                    'distance': 2000.0
                }
            ],
        },
    },
}

from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Clypeus_Genus_Name;': {
        '$Codex_Ent_Clypeus_01_Name;': {
            'name': 'Clypeus Lacrimam',
            'value': 8418000,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 196.0,
                    'min_temperature': 190.0,
                    'body_type': ['Rocky body']
                },
                {
                    'atmosphere': ['Water', 'WaterRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 455.0,
                    'min_temperature': 390.0,
                    'body_type': ['Rocky body']
                }
            ],
        },
        '$Codex_Ent_Clypeus_02_Name;': {
            'name': 'Clypeus Margaritus',
            'value': 11873200,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 196.0,
                    'min_temperature': 190.0,
                    'body_type': ['High metal content body']
                },
                {
                    'atmosphere': ['Water', 'WaterRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 455.0,
                    'min_temperature': 390.0,
                    'body_type': ['High metal content body']
                }
            ],
        },
        '$Codex_Ent_Clypeus_03_Name;': {
            'name': 'Clypeus Speculumi',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 196.0,
                    'min_temperature': 190.0,
                    'body_type': ['Rocky body'],
                    'distance': 2500.0
                },
                {
                    'atmosphere': ['Water', 'WaterRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 455.0,
                    'min_temperature': 390.0,
                    'body_type': ['Rocky body'],
                    'distance': 2500.0
                }
            ],
        },
    },
}

from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Osseus_Genus_Name;': {
        '$Codex_Ent_Osseus_01_Name;': {
            'name': 'Osseus Fractus',
            'value': 4027800,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 190.0,
                    'min_temperature': 180.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'regions': ['!perseus']
                }
            ],
        },
        '$Codex_Ent_Osseus_02_Name;': {
            'name': 'Osseus Discus',
            'value': 12934900,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia', 'Argon', 'Methane'],
                    'volcanism': 'Any',
                    'max_gravity': 0.275,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                },
                {
                    'atmosphere': ['Water', 'WaterRich'],
                    'max_gravity': 0.275,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                }
            ],
        },
        '$Codex_Ent_Osseus_03_Name;': {
            'name': 'Osseus Spiralis',
            'value': 2404700,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'max_gravity': 0.275,
                    'body_type': ['Rocky body', 'High metal content body'],
                }
            ],
        },
        '$Codex_Ent_Osseus_04_Name;': {
            'name': 'Osseus Pumice',
            'value': 3156300,
            'rulesets': [
                {
                    'atmosphere': ['Argon', 'ArgonRich', 'Methane', 'MethaneRich', 'Nitrogen'],
                    'max_gravity': 0.275,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                }
            ],
        },
        '$Codex_Ent_Osseus_05_Name;': {
            'name': 'Osseus Cornibus',
            'value': 1483000,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 196.0,
                    'min_temperature': 180.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'regions': ['perseus']
                }
            ],
        },
        '$Codex_Ent_Osseus_06_Name;': {
            'name': 'Osseus Pellebantus',
            'value': 9739000,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.275,
                    'max_temperature': 196.0,
                    'min_temperature': 190.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'regions': ['!perseus']
                }
            ],
        },
    },
}

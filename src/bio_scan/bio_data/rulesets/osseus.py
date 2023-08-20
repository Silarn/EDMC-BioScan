from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Osseus_Genus_Name;': {
        '$Codex_Ent_Osseus_01_Name;': {
            'name': 'Osseus Fractus',
            'value': 4027800,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 180.0,
                    'max_temperature': 190.0,
                    'min_pressure': 0.025,
                    'volcanism': 'None',
                    'regions': ['!perseus']
                }
            ],
        },
        '$Codex_Ent_Osseus_02_Name;': {
            'name': 'Osseus Discus',
            'value': 12934900,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.088,
                    'min_temperature': 161.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['Argon'],
                    'body_type': ['Rocky ice body'],
                    'min_gravity': 0.2,
                    'max_gravity': 0.275,
                    'min_temperature': 65.0,
                    'max_temperature': 120.0,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.127,
                    'min_temperature': 80.0,
                    'max_temperature': 110.0,
                    'min_pressure': 0.012,
                    'volcanism': 'Any'
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.055,
                    'min_temperature': 391.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.05,
                }
            ],
        },
        '$Codex_Ent_Osseus_03_Name;': {
            'name': 'Osseus Spiralis',
            'value': 2404700,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135
                }
            ],
        },
        '$Codex_Ent_Osseus_04_Name;': {
            'name': 'Osseus Pumice',
            'value': 3156300,
            'rulesets': [
                {
                    'atmosphere': ['Argon'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.059,
                    'max_gravity': 0.275,
                    'min_temperature': 50.0,
                    'max_temperature': 140.0,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['ArgonRich'],
                    'body_type': ['Rocky ice body'],
                    'min_gravity': 0.035,
                    'max_gravity': 0.1,
                    'min_temperature': 60.0,
                    'max_temperature': 80.0,
                    'min_pressure': 0.03,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.033,
                    'max_gravity': 0.275,
                    'min_temperature': 67.0,
                    'max_temperature': 109.0
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.05,
                    'max_gravity': 0.275,
                    'min_temperature': 42.0,
                    'max_temperature': 70.0,
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Osseus_05_Name;': {
            'name': 'Osseus Cornibus',
            'value': 1483000,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.0405,
                    'max_gravity': 0.275,
                    'min_temperature': 180.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.025,
                    'volcanism': 'None',
                    'regions': ['perseus']
                }
            ],
        },
        '$Codex_Ent_Osseus_06_Name;': {
            'name': 'Osseus Pellebantus',
            'value': 9739000,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.0405,
                    'max_gravity': 0.275,
                    'min_temperature': 191.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.057,
                    'volcanism': 'None',
                    'regions': ['!perseus']
                }
            ],
        },
    },
}

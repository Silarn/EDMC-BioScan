from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Conchas_Genus_Name;': {
        '$Codex_Ent_Conchas_01_Name;': {
            'name': 'Concha Renibus',
            'value': 4572400,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.045,
                    'min_temperature': 176.0,
                    'max_temperature': 177.0,
                    'volcanism': ['silicate', 'metallic']
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.276,
                    'min_temperature': 180.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.025,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.15,
                    'min_temperature': 79.0,
                    'max_temperature': 100.0,
                    'min_pressure': 0.01,
                    'volcanism': ['silicate', 'metallic']
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.65,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.65,
                    'volcanism': ['water']
                }
            ],
        },
        '$Codex_Ent_Conchas_02_Name;': {
            'name': 'Concha Aureolas',
            'value': 7774700,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.276,
                    'min_temperature': 152.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135
                }
            ],
        },
        '$Codex_Ent_Conchas_03_Name;': {
            'name': 'Concha Labiata',
            'value': 2352400,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.276,
                    'min_temperature': 150.0,
                    'max_temperature': 200.0,
                    'min_pressure': 0.002,
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Conchas_04_Name;': {
            'name': 'Concha Biconcavis',
            'value': 16777215,
            'rulesets': [
                {
                    'atmosphere': ['Nitrogen'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.276,
                    'min_temperature': 42.0,
                    'max_temperature': 51.0,
                    'max_pressure': 0.0046,
                    'volcanism': 'None'
                }
            ],
        },
    },
}

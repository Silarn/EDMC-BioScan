from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Aleoids_Genus_Name;': {
        '$Codex_Ent_Aleoids_01_Name;': {
            'name': 'Aleoida Arcus',
            'value': 7252500,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 175.0,
                    'max_temperature': 180.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Aleoids_02_Name;': {
            'name': 'Aleoida Coronamus',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 180.0,
                    'max_temperature': 190.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Aleoids_03_Name;': {
            'name': 'Aleoida Spica',
            'value': 3385200,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 170.0,
                    'max_temperature': 177.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'regions': ['scutum-centaurus']
                }
            ],
        },
        '$Codex_Ent_Aleoids_04_Name;': {
            'name': 'Aleoida Laminiae',
            'value': 3385200,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 152.0,
                    'max_temperature': 177.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'regions': ['!scutum-centaurus']
                }
            ],
        },
        '$Codex_Ent_Aleoids_05_Name;': {
            'name': 'Aleoida Gravis',
            'value': 12934900,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 190.0,
                    'max_temperature': 196.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'volcanism': 'None'
                }
            ],
        }
    },
}

from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Cactoid_Genus_Name;': {
        '$Codex_Ent_Cactoid_01_Name;': {
            'name': 'Cactoida Cortexum',
            'value': 3667600,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 180.0,
                    'max_temperature': 195.0,
                    'min_pressure': 0.025,
                    'volcanism': 'None',
                    'regions': ['orion-cygnus']
                }
            ],
        },
        '$Codex_Ent_Cactoid_02_Name;': {
            'name': 'Cactoida Lapis',
            'value': 2483600,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135,
                    'regions': ['sagittarius-carina']
                }
            ],
        },
        '$Codex_Ent_Cactoid_03_Name;': {
            'name': 'Cactoida Vermis',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': ['SulphurDioxide'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.265,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 210.0,
                    'max_pressure': 0.002,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.05,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.05,
                    'volcanism': ['water']
                }
            ],
        },
        '$Codex_Ent_Cactoid_04_Name;': {
            'name': 'Cactoida Pullulanta',
            'value': 3667600,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 180.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.025,
                    'volcanism': 'None',
                    'regions': ['perseus']
                }
            ],
        },
        '$Codex_Ent_Cactoid_05_Name;': {
            'name': 'Cactoida Peperatis',
            'value': 2483600,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135,
                    'regions': ['scutum-centaurus']
                }
            ],
        },
    },
}

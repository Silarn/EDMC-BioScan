from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Cactoid_Genus_Name;': {
        '$Codex_Ent_Cactoid_01_Name;': {
            'name': 'Cactoida Cortexum',
            'value': 3667600,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 180.0,
                    'max_temperature': 195.0,
                    'body_type': ['Rocky body', 'High metal content body'],
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
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 177.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'regions': ['sagittarius-carina']
                }
            ],
        },
        '$Codex_Ent_Cactoid_03_Name;': {
            'name': 'Cactoida Vermis',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.265,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 210.0,
                    'body_type': ['Rocky body'],
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Cactoid_04_Name;': {
            'name': 'Cactoida Pullulanta',
            'value': 3667600,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 180.0,
                    'max_temperature': 196.0,
                    'body_type': ['Rocky body', 'High metal content body'],
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
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 177.0,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'regions': ['scutum-centaurus']
                }
            ],
        },
    },
}

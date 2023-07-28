from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Shrubs_Genus_Name;': {
        '$Codex_Ent_Shrubs_01_Name;': {
            'name': 'Frutexa Flabellum',
            'value': 1808900,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 152.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135,
                    'regions': ['!scutum-centaurus']
                }
            ],
        },
        '$Codex_Ent_Shrubs_02_Name;': {
            'name': 'Frutexa Acus',
            'value': 7774700,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.237,
                    'min_temperature': 146.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.003,
                    'volcanism': 'None',
                    'regions': ['orion-cygnus']
                }
            ],
        },
        '$Codex_Ent_Shrubs_03_Name;': {
            'name': 'Frutexa Metallicum',
            'value': 1632500,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 152.0,
                    'max_temperature': 176.0,
                    'max_pressure': 0.01,
                    'volcanism': 'None',
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 146.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.002,
                    'volcanism': 'None',
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['High metal content body'],
                    'min_gravity': 0.055,
                    'max_gravity': 0.07,
                    'min_temperature': 395.0,
                    'max_temperature': 400.0,
                    'min_pressure': 0.05,
                    'max_pressure': 0.07,
                    'volcanism': 'None',
                }
            ],
        },
        '$Codex_Ent_Shrubs_04_Name;': {
            'name': 'Frutexa Flammasis',
            'value': 10326000,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 152.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135,
                    'regions': ['scutum-centaurus']
                }
            ],
        },
        '$Codex_Ent_Shrubs_05_Name;': {
            'name': 'Frutexa Fera',
            'value': 1632500,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 146.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.003,
                    'volcanism': 'None',
                    'regions': ['outer']
                }
            ],
        },
        '$Codex_Ent_Shrubs_06_Name;': {
            'name': 'Frutexa Sponsae',
            'value': 5988000,
            'rulesets': [
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.056,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.05,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.056,
                    'min_temperature': 392.0,
                    'max_temperature': 452.0,
                    'min_pressure': 0.05,
                    'volcanism': ['water']
                }
            ],
        },
        '$Codex_Ent_Shrubs_07_Name;': {
            'name': 'Frutexa Collum',
            'value': 1639800,
            'rulesets': [
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 132.0,
                    'max_temperature': 215.0,
                    'max_pressure': 0.004,
                    'body_type': ['Rocky body']
                }
            ],
        },
    },
}

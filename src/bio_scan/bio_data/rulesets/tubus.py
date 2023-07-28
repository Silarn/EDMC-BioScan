from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Tubus_Genus_Name;': {
        '$Codex_Ent_Tubus_01_Name;': {
            'name': 'Tubus Conifer',
            'value': 2415500,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.041,
                    'max_gravity': 0.152,
                    'min_temperature': 160.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.003,
                    'volcanism': 'None',
                    'regions': ['perseus']
                },
            ],
        },
        '$Codex_Ent_Tubus_02_Name;': {
            'name': 'Tubus Sororibus',
            'value': 5727600,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['High metal content body'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.152,
                    'min_temperature': 160.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135,
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['High metal content body'],
                    'min_gravity': 0.045,
                    'max_gravity': 0.152,
                    'min_temperature': 160.0,
                    'max_temperature': 189.0,
                    'volcanism': 'None'
                }
            ],
        },
        '$Codex_Ent_Tubus_03_Name;': {
            'name': 'Tubus Cavas',
            'value': 11873200,
            'rulesets': [
                {
                    'body_type': ['Rocky body'],
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.041,
                    'max_gravity': 0.152,
                    'min_temperature': 160.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.003,
                    'volcanism': 'None',
                    'regions': ['scutum-centaurus']
                },
            ],
        },
        '$Codex_Ent_Tubus_04_Name;': {
            'name': 'Tubus Rosarium',
            'value': 2637500,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.153,
                    'min_temperature': 160.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135
                },
            ],
        },
        '$Codex_Ent_Tubus_05_Name;': {
            'name': 'Tubus Compagibus',
            'value': 7774700,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.153,
                    'min_temperature': 160.0,
                    'max_temperature': 196.0,
                    'min_pressure': 0.003,
                    'volcanism': 'None',
                    'regions': ['sagittarius-carina']
                },
            ],
        },
    },
}

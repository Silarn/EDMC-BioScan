from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Tubus_Genus_Name;': {
        '$Codex_Ent_Tubus_01_Name;': {
            'name': 'Tubus Conifer',
            'value': 2415500,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.153,
                    'max_temperature': 190.0,
                    'min_temperature': 160.0,
                    'body_type': ['Rocky body'],
                    'regions': ['perseus']
                },
            ],
        },
        '$Codex_Ent_Tubus_02_Name;': {
            'name': 'Tubus Sororibus',
            'value': 5727600,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia', 'CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.153,
                    'max_temperature': 189.0,
                    'min_temperature': 160.0,
                    'body_type': ['High metal content body']
                },
            ],
        },
        '$Codex_Ent_Tubus_03_Name;': {
            'name': 'Tubus Cavas',
            'value': 11873200,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.153,
                    'max_temperature': 195.1,
                    'min_temperature': 160.0,
                    'body_type': ['Rocky body'],
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
                    'max_gravity': 0.153,
                    'max_temperature': 177.0,
                    'min_temperature': 160.0,
                    'body_type': ['Rocky body']
                },
            ],
        },
        '$Codex_Ent_Tubus_05_Name;': {
            'name': 'Tubus Compagibus',
            'value': 7774700,
            'rulesets': [
                {
                    'atmosphere': ['CarbonDioxide', 'CarbonDioxideRich'],
                    'max_gravity': 0.153,
                    'max_temperature': 196.1,
                    'min_temperature': 160.0,
                    'body_type': ['Rocky body'],
                    'regions': ['sagittarius-carina']
                },
            ],
        },
    },
}

from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Fungoids_Genus_Name;': {
        '$Codex_Ent_Fungoids_01_Name;': {
            'name': 'Fungoida Setisis',
            'value': 1670100,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia', 'Methane', 'MethaneRich'],
                    'max_gravity': 0.275,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Fungoids_02_Name;': {
            'name': 'Fungoida Stabitis',
            'value': 2680300,
            'rulesets': [
                {
                    'atmosphere': ['Methane'],
                    'max_gravity': 0.275,
                    'min_gravity': 0.041,
                    'max_temperature': 100.0,
                    'min_temperature': 80.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'regions': ['orion-cygnus']
                },
                {
                    'atmosphere': ['Water'],
                    'max_gravity': 0.275,
                    'min_gravity': 0.041,
                    'max_temperature': 452.0,
                    'min_temperature': 395.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'regions': ['orion-cygnus']
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'max_gravity': 0.275,
                    'min_gravity': 0.041,
                    'max_temperature': 196.0,
                    'min_temperature': 180.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'regions': ['orion-cygnus']
                }
            ],
        },
        '$Codex_Ent_Fungoids_03_Name;': {
            'name': 'Fungoida Bullarum',
            'value': 3703200,
            'rulesets': [
                {
                    'atmosphere': ['Argon', 'ArgonRich', 'Nitrogen', 'NitrogenRich'],
                    'max_gravity': 0.275,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Fungoids_04_Name;': {
            'name': 'Fungoida Gelata',
            'value': 3330300,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'max_gravity': 0.275,
                    'max_temperature': 180.0,
                    'min_temperature': 160.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'regions': ['!orion-cygnus-core']
                },
                {
                    'atmosphere': ['Methane'],
                    'max_gravity': 0.275,
                    'max_temperature': 110.0,
                    'min_temperature': 80.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'regions': ['!orion-cygnus-core']
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'max_gravity': 0.275,
                    'max_temperature': 196.0,
                    'min_temperature': 180.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'regions': ['!orion-cygnus-core']
                },
                {
                    'atmosphere': ['Water'],
                    'max_gravity': 0.275,
                    'max_temperature': 395.0,
                    'min_temperature': 455.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'regions': ['!orion-cygnus-core']
                }
            ],
        },
    },
}

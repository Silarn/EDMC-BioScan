from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Fungoids_Genus_Name;': {
        '$Codex_Ent_Fungoids_01_Name;': {
            'name': 'Fungoida Setisis',
            'value': 1670100,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.276,
                    'min_temperature': 152.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Rocky ice body'],
                    'min_gravity': 0.033,
                    'max_gravity': 0.276,
                    'min_temperature': 68.0,
                    'max_temperature': 109.0,
                    'volcanism': 'None'
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.033,
                    'max_gravity': 0.276,
                    'min_temperature': 67.0,
                    'max_temperature': 109.0
                }
            ],
        },
        '$Codex_Ent_Fungoids_02_Name;': {
            'name': 'Fungoida Stabitis',
            'value': 2680300,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'Rocky ice body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.045,
                    'min_temperature': 172.0,
                    'max_temperature': 177.0,
                    'volcanism': ['silicate'],
                    'regions': ['orion-cygnus']
                },
                {
                    'atmosphere': ['Argon'],
                    'body_type': ['Rocky ice body'],
                    'min_gravity': 0.20,
                    'max_gravity': 0.23,
                    'min_temperature': 60.0,
                    'max_temperature': 90.0,
                    'volcanism': ['silicate', 'rocky'],
                    'regions': ['orion-cygnus']
                },
                { # Only one sample
                    'atmosphere': ['ArgonRich'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.3,
                    'max_gravity': 0.5,
                    'min_temperature': 60.0,
                    'max_temperature': 90.0,
                    'regions': ['orion-cygnus']
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.0405,
                    'max_gravity': 0.27,
                    'min_temperature': 180.0,
                    'max_temperature': 197.0,
                    'min_pressure': 0.025,
                    'volcanism': 'None',
                    'regions': ['orion-cygnus']
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.043,
                    'max_gravity': 0.126,
                    'min_temperature': 78.5,
                    'max_temperature': 109.0,
                    'min_pressure': 0.012,
                    'volcanism': ['major silicate'],
                    'regions': ['orion-cygnus']
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.039,
                    'max_gravity': 0.064,
                    'volcanism': 'None',
                    'regions': ['orion-cygnus']
                }
            ],
        },
        '$Codex_Ent_Fungoids_03_Name;': {
            'name': 'Fungoida Bullarum',
            'value': 3703200,
            'rulesets': [
                {
                    'atmosphere': ['Argon'],
                    'min_gravity': 0.058,
                    'max_gravity': 0.276,
                    'min_temperature': 50.0,
                    'max_temperature': 129.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'volcanism': 'None',
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'min_gravity': 0.155,
                    'max_gravity': 0.276,
                    'min_temperature': 50.0,
                    'max_temperature': 70.0,
                    'body_type': ['Rocky body', 'Rocky ice body', 'High metal content body'],
                    'volcanism': 'None',
                }
            ],
        },
        '$Codex_Ent_Fungoids_04_Name;': {
            'name': 'Fungoida Gelata',
            'value': 3330300,
            'rulesets': [
                { # Only one sample - review
                    'atmosphere': ['Argon'],
                    'body_type': ['Rocky body', 'Rocky ice body'],
                    'min_gravity': 0.041,
                    'max_gravity': 0.276,
                    'min_temperature': 160.0,
                    'max_temperature': 180.0,
                    'max_pressure': 0.0135,
                    'volcanism': ['major silicate'],
                    'regions': ['!orion-cygnus-core']
                },
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['Rocky body', 'Rocky ice body'],
                    'min_gravity': 0.042,
                    'max_gravity': 0.071,
                    'min_temperature': 160.0,
                    'max_temperature': 180.0,
                    'max_pressure': 0.0135,
                    'volcanism': ['major silicate'],
                    'regions': ['!orion-cygnus-core']
                },
                {
                    'atmosphere': ['Ammonia'],
                    'body_type': ['High metal content body'],
                    'min_gravity': 0.042,
                    'max_gravity': 0.071,
                    'min_temperature': 160.0,
                    'max_temperature': 180.0,
                    'max_pressure': 0.0135,
                    'volcanism': ['major rocky'],
                    'regions': ['!orion-cygnus-core']
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.041,
                    'max_gravity': 0.276,
                    'min_temperature': 180.0,
                    'max_temperature': 200.0,
                    'min_pressure': 0.025,
                    'body_type': ['Rocky body', 'High metal content body'],
                    'volcanism': 'None',
                    'regions': ['!orion-cygnus-core']
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.044,
                    'max_gravity': 0.125,
                    'min_temperature': 80.0,
                    'max_temperature': 110.0,
                    'min_pressure': 0.01,
                    'volcanism': ['major silicate', 'major metallic'],
                    'regions': ['!orion-cygnus-core']
                },
                {
                    'atmosphere': ['Water'],
                    'body_type': ['Rocky body', 'High metal content body'],
                    'min_gravity': 0.039,
                    'max_gravity': 0.063,
                    'volcanism': 'None',
                    'regions': ['!orion-cygnus-core']
                }
            ],
        },
    },
}

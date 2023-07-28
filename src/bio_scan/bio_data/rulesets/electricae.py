from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Electricae_Genus_Name;': {
        '$Codex_Ent_Electricae_01_Name;': {
            'name': 'Electricae Pluma',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': ['Argon', 'ArgonRich'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.275,
                    'min_temperature': 50.0,
                    'max_temperature': 150.0,
                    'parent_star': ['A', 'N', 'D', 'H', 'AeBe']
                },
                {
                    'atmosphere': ['Neon', 'NeonRich'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.275,
                    'min_temperature': 20.0,
                    'max_temperature': 70.0,
                    'max_pressure': 0.005,
                    'parent_star': ['A', 'N', 'D', 'H', 'AeBe']
                }
            ],
        },
        '$Codex_Ent_Electricae_02_Name;': {
            'name': 'Electricae Radialem',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': ['Argon', 'ArgonRich'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.275,
                    'min_temperature': 50.0,
                    'max_temperature': 150.0,
                    'body_type': ['Icy body'],
                    'nebula': True
                },
                {
                    'atmosphere': ['Neon', 'NeonRich'],
                    'min_gravity': 0.026,
                    'max_gravity': 0.275,
                    'min_temperature': 20.0,
                    'max_temperature': 70.0,
                    'max_pressure': 0.005,
                    'body_type': ['Icy body'],
                    'nebula': True
                }
            ],
        },
    },
}

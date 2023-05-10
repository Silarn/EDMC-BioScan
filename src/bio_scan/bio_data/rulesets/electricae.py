from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Electricae_Genus_Name;': {
        '$Codex_Ent_Electricae_01_Name;': {
            'name': 'Electricae Pluma',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': ['Neon', 'NeonRich', 'Argon', 'ArgonRich'],
                    'max_gravity': 0.275,
                    'body_type': ['Icy body'],
                    'special': 'AV'
                }
            ],
        },
        '$Codex_Ent_Electricae_02_Name;': {
            'name': 'Electricae Radialem',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': ['Neon', 'NeonRich', 'Argon', 'ArgonRich'],
                    'max_gravity': 0.275,
                    'body_type': ['Icy body'],
                    'nebula': True
                }
            ],
        },
    },
}

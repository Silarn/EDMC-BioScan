from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Recepta_Genus_Name;': {
        '$Codex_Ent_Recepta_01_Name;': {
            'name': 'Recepta Umbrux',
            'value': 12934900,
            'rulesets': [
                {
                    'atmosphere': ['SulphurDioxide', 'Oxygen', 'CarbonDioxide'],
                    'atmosphere_component': {'SulphurDioxide': 1.05},
                    'max_gravity': 0.275,
                    'body_type': ['Icy body', 'Rocky ice body', 'Rocky body']
                }
            ],
        },
        '$Codex_Ent_Recepta_02_Name;': {
            'name': 'Recepta Deltahedronix',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': ['SulphurDioxide', 'Oxygen', 'CarbonDioxide'],
                    'atmosphere_component': {'SulphurDioxide': 1.05},
                    'max_gravity': 0.275,
                    'body_type': ['Icy body', 'Rocky body', 'High metal content body']
                }
            ],
        },
        '$Codex_Ent_Recepta_03_Name;': {
            'name': 'Recepta Conditivus',
            'value': 14313700,
            'rulesets': [
                {
                    'atmosphere': ['SulphurDioxide', 'Oxygen', 'CarbonDioxide'],
                    'atmosphere_component': {'SulphurDioxide': 1.05},
                    'max_gravity': 0.275,
                    'body_type': ['Icy body', 'Rocky ice body']
                }
            ],
        },
    },
}

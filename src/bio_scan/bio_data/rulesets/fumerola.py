from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Fumerolas_Genus_Name;': {
        '$Codex_Ent_Fumerolas_01_Name;': {
            'name': 'Fumerola Carbosis',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': ['Argon'],
                    'min_gravity': 0.168,
                    'max_gravity': 0.275,
                    'min_temperature': 57.0,
                    'max_temperature': 150.0,
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'volcanism': ['carbon', 'methane']
                },
                {
                    'atmosphere': ['Methane'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.047,
                    'min_temperature': 84.0,
                    'max_temperature': 110.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['methane magma']
                },
                {
                    'atmosphere': ['Neon'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.275,
                    'min_temperature': 40.0,
                    'max_temperature': 60.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['carbon', 'methane']
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'min_gravity': 0.2,
                    'max_gravity': 0.275,
                    'min_temperature': 57.0,
                    'max_temperature': 70.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['carbon', 'methane']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 180.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['carbon']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.19,
                    'max_gravity': 0.275,
                    'min_temperature': 149.0,
                    'max_temperature': 272.0,
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'volcanism': ['carbon']
                },
                {  # Probably incomplete
                    'atmosphere': ['Ammonia', 'ArgonRich', 'CarbonDioxideRich'],
                    'max_gravity': 0.275,
                    'body_type': ['Icy body'],
                    'volcanism': ['carbon']
                }
            ],
        },
        '$Codex_Ent_Fumerolas_02_Name;': {
            'name': 'Fumerola Extremus',
            'value': 16202800,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.09,
                    'min_temperature': 161.0,
                    'max_temperature': 177.0,
                    'body_type': ['Rock body', 'Rocky ice body', 'High metal content body'],
                    'volcanism': ['silicate', 'metallic', 'rocky']
                },
                {
                    'atmosphere': ['Argon'],
                    'min_gravity': 0.07,
                    'max_gravity': 0.275,
                    'min_temperature': 50.0,
                    'max_temperature': 90.0,
                    'body_type': ['Rock body', 'Rocky ice body', 'High metal content body'],
                    'volcanism': ['silicate', 'metallic', 'rocky']
                },
                {
                    'atmosphere': ['Methane'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.127,
                    'min_temperature': 77.0,
                    'max_temperature': 109.0,
                    'body_type': ['Rock body', 'Rocky ice body', 'High metal content body'],
                    'volcanism': ['silicate', 'metallic', 'rocky']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.07,
                    'max_gravity': 0.275,
                    'min_temperature': 54.0,
                    'max_temperature': 210.0,
                    'body_type': ['Rock body', 'Rocky ice body', 'High metal content body'],
                    'volcanism': ['silicate', 'metallic', 'rocky']
                }
            ],
        },
        '$Codex_Ent_Fumerolas_03_Name;': {
            'name': 'Fumerola Nitris',
            'value': 7500900,
            'rulesets': [
                {
                    'atmosphere': ['Argon', 'ArgonRich', 'NeonRich'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 50.0,
                    'max_temperature': 128.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['Methane'],
                    'min_gravity': 0.032,
                    'max_gravity': 0.1,
                    'min_temperature': 83.0,
                    'max_temperature': 109.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen']
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'min_gravity': 0.21,
                    'max_gravity': 0.275,
                    'min_temperature': 60.0,
                    'max_temperature': 81.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'max_gravity': 0.275,
                    'min_temperature': 150.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.21,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 250.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['nitrogen', 'ammonia']
                },
            ],
        },
        '$Codex_Ent_Fumerolas_04_Name;': {
            'name': 'Fumerola Aquatis',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': ['Ammonia'],
                    'min_gravity': 0.028,
                    'max_gravity': 0.275,
                    'min_temperature': 161.0,
                    'max_temperature': 177.0,
                    'body_type': ['Icy body', 'Rocky ice body', 'Rocky body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Argon', 'ArgonRich'],
                    'min_gravity': 0.166,
                    'max_gravity': 0.275,
                    'min_temperature': 57.0,
                    'max_temperature': 150.0,
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'min_gravity': 0.25,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 180.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Methane'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 80.0,
                    'max_temperature': 100.0,
                    'body_type': ['Rocky body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Neon'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.275,
                    'min_temperature': 20.0,
                    'max_temperature': 60.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'min_gravity': 0.195,
                    'max_gravity': 0.245,
                    'min_temperature': 56.0,
                    'max_temperature': 80.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'min_gravity': 0.23,
                    'max_gravity': 0.275,
                    'min_temperature': 153.0,
                    'max_temperature': 190.0,
                    'body_type': ['Icy body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'min_gravity': 0.18,
                    'max_gravity': 0.275,
                    'min_temperature': 150.0,
                    'max_temperature': 270.0,
                    'body_type': ['Icy body', 'Rocky ice body', 'Rocky body'],
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Water'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.06,
                    'min_temperature': 406.0,
                    'max_temperature': 450.0,
                    'body_type': ['Rocky body'],
                    'volcanism': ['water']
                }
            ],
        },
    },
}

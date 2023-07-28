from typing import Mapping

catalog: dict[str, dict[str, Mapping]] = {
    '$Codex_Ent_Fumerolas_Genus_Name;': {
        '$Codex_Ent_Fumerolas_01_Name;': {
            'name': 'Fumerola Carbosis',
            'value': 6284600,
            'rulesets': [
                {
                    'atmosphere': ['Argon'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.168,
                    'max_gravity': 0.275,
                    'min_temperature': 57.0,
                    'max_temperature': 150.0,
                    'volcanism': ['carbon', 'methane']
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.025,
                    'max_gravity': 0.047,
                    'min_temperature': 84.0,
                    'max_temperature': 110.0,
                    'min_pressure': 0.03,
                    'volcanism': ['methane magma']
                },
                {
                    'atmosphere': ['Neon'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.275,
                    'min_temperature': 40.0,
                    'max_temperature': 60.0,
                    'volcanism': ['carbon', 'methane']
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.2,
                    'max_gravity': 0.275,
                    'min_temperature': 57.0,
                    'max_temperature': 70.0,
                    'volcanism': ['carbon', 'methane']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 180.0,
                    'volcanism': ['carbon']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.19,
                    'max_gravity': 0.275,
                    'min_temperature': 149.0,
                    'max_temperature': 272.0,
                    'volcanism': ['carbon']
                },
                {  # Probably incomplete
                    'atmosphere': ['Ammonia', 'ArgonRich', 'CarbonDioxideRich'],
                    'body_type': ['Icy body'],
                    'max_gravity': 0.275,
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
                    'body_type': ['Rock body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.09,
                    'min_temperature': 161.0,
                    'max_temperature': 177.0,
                    'max_pressure': 0.0135,
                    'volcanism': ['silicate', 'metallic', 'rocky']
                },
                {
                    'atmosphere': ['Argon'],
                    'body_type': ['Rock body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.07,
                    'max_gravity': 0.275,
                    'min_temperature': 50.0,
                    'max_temperature': 90.0,
                    'volcanism': ['silicate', 'metallic', 'rocky']
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Rock body', 'Rocky ice body', 'High metal content body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.127,
                    'min_temperature': 77.0,
                    'max_temperature': 109.0,
                    'min_pressure': 0.01,
                    'volcanism': ['silicate', 'metallic', 'rocky']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'body_type': ['Rock body', 'Rocky ice body'],
                    'min_gravity': 0.07,
                    'max_gravity': 0.275,
                    'min_temperature': 54.0,
                    'max_temperature': 210.0,
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
                    'body_type': ['Icy body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 50.0,
                    'max_temperature': 128.0,
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.032,
                    'max_gravity': 0.1,
                    'min_temperature': 83.0,
                    'max_temperature': 109.0,
                    'volcanism': ['nitrogen']
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.21,
                    'max_gravity': 0.275,
                    'min_temperature': 60.0,
                    'max_temperature': 81.0,
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Icy body'],
                    'max_gravity': 0.275,
                    'min_temperature': 150.0,
                    'volcanism': ['nitrogen', 'ammonia']
                },
                {
                    'atmosphere': ['SulphurDioxide'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.21,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 250.0,
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
                    'body_type': ['Icy body', 'Rocky ice body', 'Rocky body'],
                    'min_gravity': 0.028,
                    'max_gravity': 0.275,
                    'min_temperature': 161.0,
                    'max_temperature': 177.0,
                    'min_pressure': 0.002,
                    'max_pressure': 0.02,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Argon', 'ArgonRich'],
                    'body_type': ['Icy body', 'Rocky ice body'],
                    'min_gravity': 0.166,
                    'max_gravity': 0.275,
                    'min_temperature': 57.0,
                    'max_temperature': 150.0,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['CarbonDioxide'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.25,
                    'max_gravity': 0.275,
                    'min_temperature': 160.0,
                    'max_temperature': 180.0,
                    'min_pressure': 0.01,
                    'max_pressure': 0.03,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Methane'],
                    'body_type': ['Rocky body'],
                    'min_gravity': 0.04,
                    'max_gravity': 0.275,
                    'min_temperature': 80.0,
                    'max_temperature': 100.0,
                    'min_pressure': 0.01,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Neon'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.26,
                    'max_gravity': 0.275,
                    'min_temperature': 20.0,
                    'max_temperature': 60.0,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Nitrogen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.195,
                    'max_gravity': 0.245,
                    'min_temperature': 56.0,
                    'max_temperature': 80.0,
                    'volcanism': ['water']
                },
                {
                    'atmosphere': ['Oxygen'],
                    'body_type': ['Icy body'],
                    'min_gravity': 0.23,
                    'max_gravity': 0.275,
                    'min_temperature': 153.0,
                    'max_temperature': 190.0,
                    'min_pressure': 0.01,
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
                    'min_pressure': 0.06,
                    'body_type': ['Rocky body'],
                    'volcanism': ['water']
                }
            ],
        },
    },
}


class ACSpecs():
    def __init__(self):
        self._daikin_models = ["Standard", "Pro", "Deluxe"]
        self._koppel_models = ["Standard", "Pro", "Deluxe"]
        self._lg_models = ["Standard", "Pro", "Deluxe"]
        self._samsumg_models = ["Standard", "Pro", "Deluxe"]
        self._midea_models = ["Celest", "Celest Pro", "Avigator", "Airstill Pro"]

class ACStandardMaterials():
    def __init__(self):
        self._midea = {
            "Celest": {
                "1.0": {
                    "Indoor": [],
                    "Outdoor": [],
                    "Drainage": [],
                    "Supply": [],
                },
            },
            "Avigator": {},
            "Airstill Pro": {},
        }

ims_roles = ['Admin', 'Owner/Manager', 'Technician']

employees = ["Santiago", "Raymond", "Jhun", "Stephen"]

aircon_brands = ["Daikin", "Koppel", "LG", "Midea", "Samsung", "Other"]

aircon_hps = ["0.5", "0.6", "0.8", "1", "1.5", "2.0", "2.5", "3.0", "3.0", "more"]

_midea = {
    # ------------------- WM INVERTER ----------------------- #
    "split_type_inverter_celest": {
        "1.0": {
            "Model Number": "MSCE-10CRFN8",
            "Refrigerant Piping": ("1/4", "3/8"),
            "Refrigerant Type": "R32",
        },
        "1.5": {
            "Model Number": "MSCE-13CRFN8",
            "Refrigerant Piping": ("1/4", "3/8"),
            "Refrigerant Type": "R32",
        },
        "2.0": {
            "Model Number": "MSCE-19CRFN8",
            "Refrigerant Piping": ("1/4", "1/2"),
            "Refrigerant Type": "R32",
        },
        "2.5": {
            "Model Number": "MSCE-22CRFN8",
            "Refrigerant Piping": ("1/4", "1/2"),
            "Refrigerant Type": "R32",
        },
        "3.0": {
            "Model Number": "MSCE-25CRFN8",
            "Refrigerant Piping": ("1/4", "1/2"),
            "Refrigerant Type": "R32",
        },
    },
    "split_type_inverter_avigator": {
        "1.0": {
            "Model Number": "MSAI-10CRFN8",
            "Refrigerant Piping": ("1/4", "3/8"),
            "Refrigerant Type": "R32",
        },
        "1.5": {
            "Model Number": "MSAI-13CRFN8",
            "Refrigerant Piping": ("1/4", "3/8"),
            "Refrigerant Type": "R32",
        },
        "2.0": {
            "Model Number": "MSAI-19CRFN8",
            "Refrigerant Piping": ("1/4", "1/2"),
            "Refrigerant Type": "R32",
        },
        "2.5": {
            "Model Number": "MSAI-22CRFN8",
            "Refrigerant Piping": ("1/4", "1/2"),
            "Refrigerant Type": "R32",
        },
        "3.0": {
            "Model Number": "MSAI-25CRFN8",
            "Refrigerant Piping": ("1/4", "1/2"),
            "Refrigerant Type": "R32/0.85",
        },
    },
    "split_type_inverter_airstillpro": {
        "1.0": {
            "Model Number": "MSAS-10CRFN8",
            "Refrigerant Piping": ("1/4", "3/8"),
            "Refrigerant Type": "R32",
        },
        "1.5": {
            "Model Number": "MSAS-13CRFN8",
            "Refrigerant Piping": ("1/4", "3/8"),
            "Refrigerant Type": "R32",
        },
        "2.0": {
            "Model Number": "MSAS-19CRFN8",
            "Refrigerant Piping": ("1/4", "1/2"),
            "Refrigerant Type": "R32",
        },
        "2.5": {
            "Model Number": "MSAS-25CRFN8",
            "Refrigerant Piping": ("3/8", "5/8"),
            "Refrigerant Type": "R32",
        },
    },

    # ------------------- WAC NON INVERTER ----------------------- #
    "window_type_noninverter_manual": {
        "0.6": {
            "Model Number": "FP-51ARA005HMNV-N5",
            "Refrigerant Type": "R32",
        },
        "2.0": {
            "Model Number": "MWTF2-18CMN1-NC0-[N]",
            "Refrigerant Type": "R410A",
        },
        "2.5": {
            "Model Number": "MWTF1-21CMN1-NC0-[N]",
            "Refrigerant Type": "R410A",
        },
    },
    "window_type_noninverter_remote": {
        "0.8": {
            "Model Number": "MWMDP-07CN8MC2",
            "Refrigerant Type": "R32",
        },
        "1.0": {
            "Model Number": "MWMDP-09CN8MC2",
            "Refrigerant Type": "R32",
        },
        "1.5": {
            "Model Number": "MWMDP-12CN8MC2",
            "Refrigerant Type": "R32",
        },
    },

    # ------------------- WAC INVERTER ----------------------- #
    "window_type_inverter_remote": {
        "0.8": {
            "Model Number": "MWWA-08CRFN8",
            "Refrigerant Type": "R32",
        },
        "1.0": {
            "Model Number": "MWWA-09CRFN8",
            "Refrigerant Type": "R32",
        },
        "1.5": {
            "Model Number": "MWWA-12CRFN8",
            "Refrigerant Type": "R32",
        },
    },
    "window_split_inverter_remote": {
        "0.8": {
            "Model Number": "MWWA-08CRFN8",
            "Refrigerant Type": "R32",
        },
        "1.0": {
            "Model Number": "MWWA-09CRFN8",
            "Refrigerant Type": "R32",
        },
        "1.5": {
            "Model Number": "MWWA-12CRFN8",
            "Refrigerant Type": "R32",
        },
    }
}

indoor_items = [
    {"name": "Copper Tube", "unit": "roll", "sizes": ["1/4", "3/8", "1/2", "5/8", "3/4", "7/8"]},
    {"name": "Rubber Insulation", "unit": "pcs", "sizes": ["1/4 x 1/2", "3/8 x 1/2", "1/2 x 1/2", "5/8 x 1/2", "7/8 x 1/2", "1/4 x 3/4", "3/8 x 3/4", "1/2 x 3/4", "5/8 x 3/4", "7/8 x 3/4"]},
    {"name": "Polytape", "unit": "pcs"},
    {"name": "Aerotape", "unit": "pcs"},
    {"name": "Electrical Tape", "unit": "pcs"},
    {"name": "Tox", "unit": ["pcs", "set"], "sizes": ["#6", "#8"]},
    {"name": "Screw", "unit": ["pcs", "set"]},
    {"name": "Dust Bag", "unit": "pcs"}
]

outdoor_items = [
    {"name": "Bracket", "unit": "pcs", "sizes": ["1HP-1.5HP"]},
    {"name": "Bolts and Nuts", "unit": "pcs", "sizes": []},
    {"name": "DynaBolt", "unit": "pcs"},
    {"name": "Expansion Bolt", "unit": "pcs"},
    {"name": "Flexible Cement", "unit": "pcs"},
    {"name": "Cable Tie", "unit": ["pcs", "set"]},
    {"name": "Cable Clamp", "unit": ["pcs", "set"]},
    {"name": "Level Bar", "unit": "pcs"},
]

supply_items = [
    {"name": "Breaker", "unit": "pcs", "sizes": ["16A", "20A", "32A", "40A"], "type": ["2-phase", "3-phase"]},
    {"name": "Breaker Box", "unit": "pcs", "sizes": ["standard"], "type": ["2-pole", "3-pole"]},
    {"name": "Royal Cord", "unit": "roll", "sizes": []},
    {"name": "PDX Wire", "unit": "roll", "sizes": []},
    {"name": "THHN Wire", "unit": "roll", "sizes": []},
    {"name": "Cable Clamp", "unit": ["pcs", "set"], "sizes": ["12mm", "14mm"], "type": ["Round", "Flat"]},
]

drainage_items = [
    {"name": "PVC Blue", "unit": "pcs", "sizes": ["1/2", "3/4"]},
    {"name": "PVC Clamp", "unit": "pcs", "sizes": ["1/2", "3/4"]},
    {"name": "PVC Elbow", "unit": "pcs", "sizes": ["1/2", "3/4"]},
    {"name": "Neltex", "unit": "pcs", "sizes": []},
    {"name": "Sealant", "unit": "pcs", "sizes": []},
]

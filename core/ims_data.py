
class ACSpecs():
    def __init__(self):
        self._ac_types = {
            "WINDOW": {
                "INVERTER": {
                    "MIDEA": {
                        "U SERIES": {"Midea U 1.0HP Window Type Inverter": 1.0, "Midea U 1.5HP Window Type Inverter": 1.5},
                        "STANDARD": {"FP-51ARA010HEIV-N4": 1.0, "FP-51ARA015HEIV-N4": 1.5},
                    },
                    "CARRIER": {
                        "OPTIMA": {"WCARZ006EC1": 0.6, "WCARZ010EC1": 1.0, "WCARZ015EC1": 1.5}
                    },
                    "KOPPEL": {
                        "KV-SERIES": {"KV09WRARF31A": 1.0, "KV12WRARF31A": 1.5, "KV18WRARF31A": 2.0},
                    },
                    "LG": {
                        "DUAL INVERTER": {"LA100GC2": 1.0, "LA150GC2": 1.5}
                    },
                },

                "NON_INVERTER": {
                    "MIDEA": {
                        "MANUAL": {"FP-51ARA006HMNV-N5": 0.6, "FP-51ARA010HMNV-N5": 1.0, "FP-51ARA015HMNV-N5": 1.5}
                    },
                    "CARRIER": {
                        "CRYSTAL": {"WCARH006EE": 0.6, "WCARH010EE": 1.0, "WCARH015EE": 1.5}
                    },
                    "KOPPEL": {
                        "EVO": {"KWR06M4A2": 0.6, "KWR09R4A2": 1.0, "KWR12R4A2": 1.5}
                    },
                    "LG": {
                        "STANDARD": { "LA100CC": 1.0}
                    },
                    "TCL": {
                        "BASIC": {"TAC-09CWM/F": 1.0, "TAC-12CWM/F": 1.5}
                    },
                },
            },
            "WALL MOUNTED": {
                "INVERTER": {
                    "MIDEA": {
                        "CELEST PRO": {"MSCE-10CRFN8": 1.0, "MSCE-13CRFN8": 1.5, "MSCE-19CRFN8": 2.0, "MSCE-22CRFN8": 2.5, "MSCE-25CRFN8": 3.0},
                        "AVIGATOR": {"MSAI-10CRFN8": 1.0, "MSAI-13CRFN8": 1.5, "MSAI-19CRFN8": 2.0, "MSAI-22CRFN8": 2.5, "MSAI-25CRFN8": 3.0},
                        "AIRSTILL PRO": {"MSAS-10CRFN8": 1.0, "MSAS-13CRFN8": 1.5, "MSAS-19CRFN8": 2.0, "MSAS-25CRFN8": 2.5},
                    }, 
                    "CARRIER": {
                        "NEO": {"FP-53NEO010EEIV": 1.0, "FP-53NEO015EEIV": 1.5, "FP-53NEO020EEIV": 2.0},
                        "OPTIMA": {"FP-53OPT010EEIV": 1.0, "FP-53OPT015EEIV": 1.5, "FP-53OPT020EEIV": 2.0},
                        "NEXUS": {"53CEA009308": 1.0, "53CEA012308": 1.5, "53CEA018308": 2.0, "53CEA024308": 2.5},
                        "FLEXISPLIT": {"FP-53FLX010EEIV": 1.0, "FP-53FLX015EEIV": 1.5, "FP-53FLX020EEIV": 2.0},
                    }, 
                    "DAIKIN": {
                        "D-SMART QUEEN": {"FTKC25TVM": 1.0, "FTKC35TVM": 1.5, "FTKC50TVM": 2.0, "FTKC60TVM": 2.5},
                        "D-SMART PRINCE": {"FTKC60TVM": 2.5, "FTKC71TVM": 3.0},
                        "D-SMART STANDARD": {"FTKQ25BVA": 1.0, "FTKQ35BVA": 1.5, "FTKQ50BVA": 2.0, "FTKQ60BVA": 2.5},
                        "D-SMART KING": {"FTKC71TVM": "3.0+"},
                    },
                    "KOPPEL":{
                        "LUNAIRE": {"KV09WMARF31D": 1.0, "KV12WMARF31D": 1.5, "KV18WMARF31D": 2.0, "KV24WMARF31D": 2.5},
                    },
                    "LG": {
                        "DUAL INVERTER": {"LA100AE2": 1.0, "LA130AE2": 1.5, "LA150GC2": 2.0},
                        "HS": {"HS09ISY2": 1.0, "HS12IPM": 1.5, "HS18IPM": 2.0, "HS24IPM": 2.5,},
                        "PREMIUM": {"HS09IPX3": 1.0, "HS12IPX3": 1.5, "HS18IPX3": 2.0, "HS24IPX3": 2.5},
                        "DELUXE": {"HS09APX3": 1.0, "HS12APX3": 1.5, "HS18APX3": 2.0, "HS24APX3": 2.5},
                    },
                    "SAMSUNG": {
                        "Windfree™": {"AR09DXDABWKN": 1.0, "AR12DXDABWKN": 1.5, "AR18DXDABWKN": 2.0, "AR24DXDABWKN": 2.5},
                        "WindFree™ BASIC": {"AR09BYHAMWKNTC": 1.0,  "AR12BYHAMWKNTC": 1.5, "AR18BYHAMWKNTC": 2.0, "AR24BYHAMWKNTC": 2.5},
                        "WindFree™ PREMIUM": {"AR10CYECABTNTC": 1.0,  "AR12CYECABTNTC": 1.5, "AR18CYECABTNTC": 2.0, "AR24CYEAAWKNTC": 2.5},
                        "DIGITAL_BASIC_S": {"AR09TYHYEWKNTC": 1.0, "AR12TYHYEWKNTC": 1.5},
                    },
                    "TCL": {
                        "KEI": {"TAC-09CSA/KEI": 1.0, "TAC-18CSA/KEI": 2.0, "TAC-24CSA/KEI": 2.5},
                        "MEI/MEI2": {"TAC-10CSD/MEI2": 1.5},
                        "FRESHIN": {"TAC-09CHSD/FAI": 1.0, "TAC-12CHSD/FAI": 1.5, "TAC-18CHSD/FAI": 2.0},
                        "T-PRO": {"TAC-09CSA/MEI": 1.0, "TAC-12CSA/MEI": 1.5, "TAC-18CSA/MEI": 2.0},
                        "BREEZEIN": {"TAC-12CSD/KEI2": 1.0, "TAC-18CSD/KEI2": 1.5, "TAC-10CSD/KEI2": 2.0},
                    },
                    "AUX": {
                        "F-SERIES": {"AUX-F1-09HP": 1.0, "AUX-F1-12HP": 1.5, "AUX-F1-18HP": 2.0, "AUX-F1-24HP": 2.5},
                        "Q-SERIES": {"AUX-QSMART-09HP": 1.0, "AUX-QSMART-12HP": 1.5, "AUX-QSMART-18HP": 2.0, "AUX-QSMART-24HP": 2.5},
                        "J-SERIES": {"ASW09A2/JADI": 1.0, "ASW12A2/JADI": 1.5, "ASW18A2/JADI": 2.0},
                        "FL-SERIES": {"ASW09A2/FL": 1.0, "ASW12A2/FL": 1.5, "ASW18A2/FL": 2.0, "ASW24A2/FL": 2.5, "ASW30A2/FL": 3.0},
                        "FF-SERIES": {"ASW09A2/FF": 1.0, "ASW12A2/FF": 1.5, "ASW18A2/FF": 2.0, "ASW24A2/FF": 2.5, "ASW30A2/FF": 3.0},
                    }, 
                },

                "NON_INVERTER": {
                    "KOPPEL": {
                        "EVO": {"KSW-09R4A2 / KPC-09HH4A2": 1.0, "KSW-12R4A2 / KPC-12HH4A2": 1.5, "KSW-18R4A2 / KPC-18HH4A2": 2.0, "KSW-24R4A2 / KPC-24HH4A2": 2.5}
                    },
                },
            },

            "FLOOR_STANDING": {
                "INVERTER": {
                    "MIDEA": {
                        "Floor Standing Inverter": {"MFSI/O-36CDN8-MD3": 3.0, "MFSI/O-52CDN8-MD1 (1 Phase)": 5.0, "MFSI/O-52CDN8-DD1 (3 Phase)": 5.0},
                    },
                    "CARRIER": {
                        "Floor Mounted Inverter": {"FP-53FMX020EEIV": 2.0, "FP-53FMX025EEIV": 2.5, "FP-53FMX030EEIV": 3.0},
                    },
                    "DAIKIN": {
                        "Floor Standing Inverter": {"FVQ50PV1B": 2.0, "FVQ60PV1B": 2.5, "FVQ71PV1B": 3.0},
                    },
                    "KOPPEL": {
                        "Floor Mounted Inverter": {"KFM-18WMARF31D": 2.0, "KFM-24WMARF31D": 2.5, "KFM-30WMARF31D": 3.0},
                    },
                    "LG": {
                        "Floor Standing Inverter": {"APNQ18GS1A": 2.0, "APNQ24GS1A": 2.5, "APNQ30GS1A": 3.0},
                    },
                    "SAMSUNG": {
                        "Floor Standing Inverter": {"AC024MNJDKG": 2.0, "AC030MNJDKG": 2.5, "AC036MNJDKG": 3.0},
                    },
                },

                "NON_INVERTER": {
                    "MIDEA": {
                        "Floor Standing Non-Inverter": {"FP-53AFS036KENV-J5": 3.0},
                    },
                    "CARRIER": {
                        "Floor Mounted Non-Inverter": {"FP-53FMX020EE": 2.0, "FP-53FMX025EE": 2.5, "FP-53FMX030EE": 3.0},
                    },
                    "KOPPEL": {
                        "Floor Mounted Non-Inverter": {"KFM-18R4A2": 2.0, "KFM-24R4A2": 2.5, "KFM-30R4A2": 3.0},
                    },
                },
            },

            "CEILING_CASSETTE": {
                "INVERTER": {
                    "MIDEA": {
                        "Ceiling Cassette Inverter": {"MCD-36HRFN1": 3.0, "MCD-48HRFN1": 4.0, "MCD-60HRFN1": 5.0}
                    },
                    "CARRIER": {
                        "Optima Cassette Inverter": {"FP-53CCS040EEIV": 4.0, "FP-53CCS050EEIV": 5.0, "FP-53CCS060EEIV": 6.0}
                    },
                    "DAIKIN": {
                        "SkyAir Inverter": {"FCQ50KAVE/RRQ50KAVE": 2.0, "FCQ60KAVE/RRQ60KAVE": 2.5, "FCQ71KAVE/RRQ71KAVE": 3.0, "FCQ100KAVE/RRQ100KAVE": 4.0, "FCQ125KAVE/RRQ125KAVE": 5.0,}
                    },
                    "KOPPEL": {
                        "Ceiling Cassette Inverter": {"KCC-36WMARF31D": 3.0, "KCC-48WMARF31D": 4.0, "KCC-60WMARF31D": 5.0}
                    },
                    "LG": {
                        "Ceiling Cassette Inverter": {"ATNQ18GULA": 2.0, "ATNQ24GULA": 2.5, "ATNQ30GULA": 3.0}
                    },
                    "SAMSUNG": {
                        "4-Way Cassette Inverter": {"AC052MN4PKG": 2.0, "AC071MN4PKG": 2.5, "AC100MN4PKG": 3.0}
                    },
                },

                "NON_INVERTER": {
                    "MIDEA": {
                        "Ceiling Cassette Non-Inverter": {"MCD-36HRN1": 3.0, "MCD-48HRN1": 4.0, "MCD-60HRN1": 5.0}
                    },
                    "CARRIER": {
                        "Optima Cassette Non-Inverter": {"FP-53CCS040EE": 4.0, "FP-53CCS050EE": 5.0, "FP-53CCS060EE": 6.0}
                    },
                    "DAIKIN": {
                        "SkyAir Non-Inverter": {"FCRN50AXVL/RR50AGXVL": 2.0, "FCRN60AXVL/RR60AGXVL": 2.5, "FCRN71AXVL/RR71AGXVL": 3.0, "FCRN100AXVL/RR100AGXVL": 4.0, "FCRN125AXVL/RR125AGXVL": 5.0,}
                    },
                    "KOPPEL": {
                        "Ceiling Cassette Non-Inverter": {"KCC-36R4A2": 3.0, "KCC-48R4A2": 4.0, "KCC-60R4A2": 5.0}
                    },
                },
            },
        }

        # AC SERIES
        self._series = {
            "MIDEA": ["Celest Pro", "Avigator", "Airstill Pro"],
            "CARRIER": ["Carrier Aura", "Carrier Neo", "Carrier FlexiSplit", "Carrier Alpha", "Carrier Optima", "Carrier Crystal 2"],
            "DAIKIN": ["D-Smart Queen", "D-Smart (Standard)", "D-Smart Prince"],
            "KOPPEL": ["Viva Series", "EVO Series", "Era Series", "Super Inverter/Lunaire Series", "KV-Series"],
            "LG": ["HS-/HSN Series", "Dual Inverter Standard", "Premium / Deluxe"],
            "SAMSUNG": ["Windfree™", "WindFree Premium", "Basic / WindFree", "Digital Basic S", "DVM S2 (VRF)"],
            "TCL": ["KEI Series", "MEI / MEI2 Series", "FreshIN", "T-Pro Series", "BreezeIN Series"],
            "AUX": ["F-Series", "J-Series", "Q-Series", "FL Series", "FF Series"]
        }

        # AC MODELS
        self._models = {
            "MIDEA": {
                "CELEST PRO": ["MSCE-10CRFN8", "MSCE-13CRFN8", "MSCE-19CRFN8", "MSCE-22CRFN8", "MSCE-25CRFN8"],
                "AVIGATOR": ["MSAI-10CRFN8", "MSAI-13CRFN8", "MSAI-19CRFN8", "MSAI-22CRFN8", "MSAI-25CRFN8"],
                "AIRSTILL PRO": ["MSAS-10CRFN8", "MSAS-13CRFN8", "MSAS-19CRFN8", "MSAS-25CRFN8"]
                },
            "CARRIER": {
                "CARRIER AURA": ["",],
                "CARRIER NEO": ["",],
                "CARRIER FLEXISPLIT": ["",],
                "CARRIER ALPHA": ["",],
                "CARRIER OPTIMA": ["",],
                "CARRIER CRYSTAL 2": ["",],
                },
            "DAIKIN": {
                "D-SMART QUEEN": ["",],
                "D-SMART (STANDARD)": ["",],
                "D-SMART PRINCE": ["",],
                },
            "KOPPEL": {
                "VIVA SERIES": ["",],
                "EVO SERIES": ["",],
                "ERA SERIES": ["",],
                "S-INV/LUNAIRE SERIES": ["",],
                "KV-SERIES": ["",],
                },
            "LG": {
                "HS-/HSN SERIES": ["",],
                "DUAL INVERTER STANDARD": ["",],
                "PREMIUM / DELUXE": ["",],
                },
            "SAMSUNG": {
                "WINDFREE™": ["",],
                "WINDFREE PREMIUM": ["",],
                "BASIC / WINDFREE": ["",],
                "DIGITAL BASIC S": ["",],
                "DVM S2 (VRF)": ["",],
                },
            "TCL": {
                "KEI SERIES": ["",],
                "MEI / MEI2 SERIES": ["",],
                "FRESHIN": ["",],
                "T-PRO SERIES": ["",],
                "BREEZEIN SERIES": ["",],
                },
            "AUX": {
                "F-SERIES": ["",],
                "J-SERIES": ["",],
                "Q-SERIES": ["",],
                "FL SERIES": ["",],
                "FF SERIES": ["",],
                }, 
            }

        # HORSE POWERS
        self._aircon_hp_list = {
            "NONE": {
                "_NONE": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                }
            },
            "MIDEA": {
                "CELEST PRO": {
                    "MSCE-10CRFN8": 1.0,
                    "MSCE-13CRFN8": 1.5,
                    "MSCE-19CRFN8": 2.0,
                    "MSCE-22CRFN8": 2.5,
                    "MSCE-25CRFN8": 3.0,
                },
                "AVIGATOR": {
                    "MSAI-10CRFN8": 1.0,
                    "MSAI-13CRFN8": 1.5,
                    "MSAI-19CRFN8": 2.0,
                    "MSAI-22CRFN8": 2.5,
                    "MSAI-25CRFN8": 3.0,
                },
                "AIRSTILL PRO": {
                    "MSAS-10CRFN8": 1.0,
                    "MSAS-13CRFN8": 1.5,
                    "MSAS-19CRFN8": 2.0,
                    "MSAS-25CRFN8": 2.5,
                },
            },
            "CARRIER": {
                "CARRIER AURA": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "CARRIER NEO": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "CARRIER FLEXISPLIT": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "CARRIER ALPHA": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "CARRIER OPTIMA": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "CARRIER CRYSTAL 2": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
            },
            "DAIKIN": {
                "D-SMART QUEEN": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "D-SMART (STANDARD)": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "D-SMART PRINCE": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
            },
            "KOPPEL": {
                "VIVA SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "EVO SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "ERA SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "SUPER INVERTER/LUNAIRE SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "KV-SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
            },
            "LG": {
                "HS-/HSN SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "DUAL INVERTER STANDARD": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "PREMIUM / DELUXE": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
            },
            "SAMSUNG": {
                "WINDFREE™": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "WINDFREE PREMIUM": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "BASIC / WINDFREE": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "DIGITAL BASIC S": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "DVM S2 (VRF)": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
            },
            "TCL": {
                "KEI SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "MEI / MEI2 SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "FRESHIN": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "T-PRO SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "BREEZEIN SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
            },
            "AUX": {
                "F-SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "J-SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "Q-SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "FL SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
                "FF SERIES": {
                    "": 1.0,
                    "": 1.5,
                    "": 2.0,
                    "": 2.5,
                    "": 3.0,
                },
            },
        }
        


ims_roles = ['Admin', 'Owner/Manager', 'Technician']

field_employees = ["Santiago", "Sonny", "Bryan", "Stephen", "Kent"]

# aircon_types = ["WINDOW TYPE", "WALL MOUNTED", "FLOOR MOUNTED", "CEILING CASSETTE"]

# aircon_compressors = ["INVERTER", "NON-INVERTER"]

# aircon_brands = ['AUX', 'CARRIER', 'DAIKIN', 'KOPPEL', 'LG', 'MIDEA', 'SAMSUNG', 'TCL', 'OTHER']

aircon_hps = ["0.5", "0.6", "0.8", "1.0", "1.5", "2.0", "2.5", "3.0", "more"]

sample_data = {
    "Polytape": {"sizes": [], "stock": 20},
    "Aerotape": {"sizes": [], "stock": 20},
    "Electrical Tape": {"sizes": [], "stock": 20},
    "Tox": {"sizes": ["6mm", "8mm"], "stock": 20},
    "Screw": {"sizes": ["6mm", "8mm"], "stock": 20},
    "Dust Bag": {"sizes": [], "stock": 20},
    "Flexible Cement": {"sizes": [], "stock": 20},
}

indoor_items = [
    {"name": "Copper Tube", "unit": "roll", "sizes": ["1/4", "3/8", "1/2", "5/8", "3/4", "7/8"]},
    {"name": "Rubber Insulation", "unit": "pcs", "sizes": ["1/4 x 1/2", "3/8 x 1/2", "1/2 x 1/2", "5/8 x 1/2", "7/8 x 1/2", "1/4 x 3/4", "3/8 x 3/4", "1/2 x 3/4", "5/8 x 3/4", "7/8 x 3/4"]},
    # {"name": "Polytape", "unit": "pcs"},
    # {"name": "Aerotape", "unit": "pcs"},
    # {"name": "Electrical Tape", "unit": "pcs"},
    # {"name": "Tox", "unit": ["pcs", "set"], "sizes": ["#6", "#8"]},
    # {"name": "Screw", "unit": ["pcs", "set"]},
    # {"name": "Dust Bag", "unit": "pcs"}
]

outdoor_items = [
    {"name": "Bracket", "unit": "pcs", "sizes": ["1HP-1.5HP"]},
    {"name": "Bolts and Nuts", "unit": "pcs", "sizes": []},
    {"name": "DynaBolt", "unit": "pcs"},
    {"name": "Expansion Bolt", "unit": "pcs"},
    {"name": "Cable Tie", "unit": ["pcs", "set"]},
    {"name": "Cable Clamp", "unit": ["pcs", "set"]},
    {"name": "Flexible Cement", "unit": "pcs"},
]

supply_items = [
    {"name": "Breaker", "unit": "pcs", "sizes": ["16A", "20A", "32A", "40A"], "type": ["2-phase", "3-phase"]},
    {"name": "Breaker Box", "unit": "pcs", "sizes": ["standard"], "type": ["2-pole", "3-pole"]},
    {"name": "Royal Cord", "unit": "roll", "sizes": []},
    {"name": "PDX Wire", "unit": "roll", "sizes": []},
    {"name": "THHN Wire", "unit": "roll", "sizes": ["10/7", "12/7", "14/7"]},
    {"name": "Cable Clamp", "unit": ["pcs", "set"], "sizes": ["12mm", "14mm"], "type": ["Round", "Flat"]},
]

drainage_items = [
    {"name": "PVC Blue", "unit": "pcs", "sizes": ["1/2", "3/4"]},
    {"name": "PVC Clamp", "unit": "pcs", "sizes": ["1/2", "3/4"]},
    {"name": "PVC Elbow", "unit": "pcs", "sizes": ["1/2", "3/4"]},
    {"name": "Neltex", "unit": "pcs", "sizes": []},
    {"name": "Sealant", "unit": "pcs", "sizes": []},
]

equipment_items = [
    {"name": "Level Bar", "unit": "pcs", "sizes": ["Short", "Long"]},
    {"name": "Hammer Drill", "unit": "pcs", "sizes": []},
    {"name": "Portable Drill", "unit": "pcs", "sizes": []},
    {"name": "Flaring Tools", "unit": "pcs", "sizes": []},
    {"name": "Rachet", "unit": "pcs", "sizes": []},
    {"name": "Pressure Gauge", "unit": "pcs", "sizes": []},
    {"name": "Vacuum", "unit": "pcs", "sizes": []},
    {"name": "Maf Gas", "unit": "pcs", "sizes": []},
    {"name": "Silver Rod", "unit": "pcs", "sizes": []},
    {"name": "Welding Machine", "unit": "pcs", "sizes": []},
    {"name": "Welding Rod", "unit": "pcs", "sizes": []},
    {"name": "Cut-Off Machine", "unit": "pcs", "sizes": []},
    {"name": "Heat Gun", "unit": "pcs", "sizes": []},
    {"name": "Angle Grinder", "unit": "pcs", "sizes": []},
    {"name": "Bender Kit", "unit": "set", "sizes": []},
    {"name": "Spring Bender", "unit": "pcs", "sizes": ["1/4", "3/8", "1/2", "5/8", "3/4", "7/8"]},
    {"name": "Adjustable Wrench", "unit": "pcs", "sizes": ["S", "M", "L"]},
    {"name": "Extension", "unit": "pcs", "sizes": []},
    {"name": "Ladder", "unit": "pcs", "sizes": ["Short", "Long"]},
    {"name": "Work Gloves", "unit": "pcs", "sizes": []},
]



# class ACStandardMaterials():
#     def __init__(self):
#         self._midea = {
#             "Celest": {
#                 "1.0": {
#                     "Indoor": [],
#                     "Outdoor": [],
#                     "Drainage": [],
#                     "Supply": [],
#                 },
#             },
#             "Avigator": {},
#             "Airstill Pro": {},
#         }


# _midea = {
#     # ------------------- WM INVERTER ----------------------- #
#     "split_type_inverter_celest": {
#         "1.0": {
#             "Model Number": "MSCE-10CRFN8",
#             "Refrigerant Piping": ("1/4", "3/8"),
#             "Refrigerant Type": "R32",
#         },
#         "1.5": {
#             "Model Number": "MSCE-13CRFN8",
#             "Refrigerant Piping": ("1/4", "3/8"),
#             "Refrigerant Type": "R32",
#         },
#         "2.0": {
#             "Model Number": "MSCE-19CRFN8",
#             "Refrigerant Piping": ("1/4", "1/2"),
#             "Refrigerant Type": "R32",
#         },
#         "2.5": {
#             "Model Number": "MSCE-22CRFN8",
#             "Refrigerant Piping": ("1/4", "1/2"),
#             "Refrigerant Type": "R32",
#         },
#         "3.0": {
#             "Model Number": "MSCE-25CRFN8",
#             "Refrigerant Piping": ("1/4", "1/2"),
#             "Refrigerant Type": "R32",
#         },
#     },
#     "split_type_inverter_avigator": {
#         "1.0": {
#             "Model Number": "MSAI-10CRFN8",
#             "Refrigerant Piping": ("1/4", "3/8"),
#             "Refrigerant Type": "R32",
#         },
#         "1.5": {
#             "Model Number": "MSAI-13CRFN8",
#             "Refrigerant Piping": ("1/4", "3/8"),
#             "Refrigerant Type": "R32",
#         },
#         "2.0": {
#             "Model Number": "MSAI-19CRFN8",
#             "Refrigerant Piping": ("1/4", "1/2"),
#             "Refrigerant Type": "R32",
#         },
#         "2.5": {
#             "Model Number": "MSAI-22CRFN8",
#             "Refrigerant Piping": ("1/4", "1/2"),
#             "Refrigerant Type": "R32",
#         },
#         "3.0": {
#             "Model Number": "MSAI-25CRFN8",
#             "Refrigerant Piping": ("1/4", "1/2"),
#             "Refrigerant Type": "R32/0.85",
#         },
#     },
#     "split_type_inverter_airstillpro": {
#         "1.0": {
#             "Model Number": "MSAS-10CRFN8",
#             "Refrigerant Piping": ("1/4", "3/8"),
#             "Refrigerant Type": "R32",
#         },
#         "1.5": {
#             "Model Number": "MSAS-13CRFN8",
#             "Refrigerant Piping": ("1/4", "3/8"),
#             "Refrigerant Type": "R32",
#         },
#         "2.0": {
#             "Model Number": "MSAS-19CRFN8",
#             "Refrigerant Piping": ("1/4", "1/2"),
#             "Refrigerant Type": "R32",
#         },
#         "2.5": {
#             "Model Number": "MSAS-25CRFN8",
#             "Refrigerant Piping": ("3/8", "5/8"),
#             "Refrigerant Type": "R32",
#         },
#     },

#     # ------------------- WAC NON INVERTER ----------------------- #
#     "window_type_noninverter_manual": {
#         "0.6": {
#             "Model Number": "FP-51ARA005HMNV-N5",
#             "Refrigerant Type": "R32",
#         },
#         "2.0": {
#             "Model Number": "MWTF2-18CMN1-NC0-[N]",
#             "Refrigerant Type": "R410A",
#         },
#         "2.5": {
#             "Model Number": "MWTF1-21CMN1-NC0-[N]",
#             "Refrigerant Type": "R410A",
#         },
#     },
#     "window_type_noninverter_remote": {
#         "0.8": {
#             "Model Number": "MWMDP-07CN8MC2",
#             "Refrigerant Type": "R32",
#         },
#         "1.0": {
#             "Model Number": "MWMDP-09CN8MC2",
#             "Refrigerant Type": "R32",
#         },
#         "1.5": {
#             "Model Number": "MWMDP-12CN8MC2",
#             "Refrigerant Type": "R32",
#         },
#     },

#     # ------------------- WAC INVERTER ----------------------- #
#     "window_type_inverter_remote": {
#         "0.8": {
#             "Model Number": "MWWA-08CRFN8",
#             "Refrigerant Type": "R32",
#         },
#         "1.0": {
#             "Model Number": "MWWA-09CRFN8",
#             "Refrigerant Type": "R32",
#         },
#         "1.5": {
#             "Model Number": "MWWA-12CRFN8",
#             "Refrigerant Type": "R32",
#         },
#     },
#     "window_split_inverter_remote": {
#         "0.8": {
#             "Model Number": "MWWA-08CRFN8",
#             "Refrigerant Type": "R32",
#         },
#         "1.0": {
#             "Model Number": "MWWA-09CRFN8",
#             "Refrigerant Type": "R32",
#         },
#         "1.5": {
#             "Model Number": "MWWA-12CRFN8",
#             "Refrigerant Type": "R32",
#         },
#     }
# }
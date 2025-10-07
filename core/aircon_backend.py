import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "aircon.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def create_tables():
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS ac_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS technology (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tech_name TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT UNIQUE
        );

        CREATE TABLE series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_name TEXT NOT NULL,
            brand_id INTEGER NOT NULL,
            type_id INTEGER REFERENCES ac_types(id),
            UNIQUE(series_name, brand_id, type_id)
        );

        CREATE UNIQUE INDEX idx_series_unique 
        ON series (series_name, brand_id, type_id);

        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT,
            hp REAL,
            series_id INTEGER NULL,
            tech_id INTEGER NOT NULL,
            type_id INTEGER NOT NULL,
            FOREIGN KEY (series_id) REFERENCES series(id),
            FOREIGN KEY (tech_id) REFERENCES technology(id),
            FOREIGN KEY (type_id) REFERENCES ac_types(id),
            UNIQUE(model_name, series_id)
        );
    """)

    conn.commit()
    print("DB tables created.")

# create_tables()


def insert_model(ac_type, tech, brand=None, series=None, model_name=None, hp=None):
    """Insert a new AC model into the database with validation and duplicate prevention."""

    # ===== Normalize & Clean =====
    ac_type = ac_type.replace(" ", "_").upper().strip() if ac_type else None
    tech = tech.upper().strip() if tech else None
    brand = brand.upper().strip() if brand else None
    series = series.upper().strip() if series else None
    model_name = model_name.upper().strip() if model_name else None

    # ===== Required fields =====
    if not ac_type or not tech:
        raise ValueError("❌ AC Type and Technology are required.")
    if not model_name:
        raise ValueError("⚠️ Model name is required to save.")

    # ===== AC Type =====
    cursor.execute("INSERT OR IGNORE INTO ac_types (type_name) VALUES (?)", (ac_type,))
    cursor.execute("SELECT id FROM ac_types WHERE type_name = ?", (ac_type,))
    type_row = cursor.fetchone()
    if not type_row:
        raise ValueError(f"❌ Failed to retrieve type_id for AC Type '{ac_type}'.")
    type_id = type_row[0]

    # ===== Technology =====
    cursor.execute("INSERT OR IGNORE INTO technology (tech_name) VALUES (?)", (tech,))
    cursor.execute("SELECT id FROM technology WHERE tech_name = ?", (tech,))
    tech_row = cursor.fetchone()
    if not tech_row:
        raise ValueError(f"❌ Failed to retrieve tech_id for Technology '{tech}'.")
    tech_id = tech_row[0]

    # ===== Brand (optional) =====
    brand_id = None
    if brand:
        cursor.execute("INSERT OR IGNORE INTO brands (brand_name) VALUES (?)", (brand,))
        cursor.execute("SELECT id FROM brands WHERE brand_name = ?", (brand,))
        brand_row = cursor.fetchone()
        if not brand_row:
            raise ValueError(f"❌ Failed to retrieve brand_id for Brand '{brand}'.")
        brand_id = brand_row[0]

    # ===== Series (optional, depends on brand) =====
    series_id = None
    if series and brand_id:
        # ✅ Use type_id in both insert & select to match new UNIQUE constraint
        cursor.execute("""
            INSERT OR IGNORE INTO series (series_name, brand_id, type_id)
            VALUES (?, ?, ?)
        """, (series, brand_id, type_id))

        cursor.execute("""
            SELECT id FROM series 
            WHERE series_name = ? AND brand_id = ? AND type_id = ?
        """, (series, brand_id, type_id))
        series_row = cursor.fetchone()
        if not series_row:
            raise ValueError(
                f"❌ Failed to retrieve series_id for series='{series}', brand_id={brand_id}, type_id={type_id}"
            )
        series_id = series_row[0]

    # ===== Check for duplicates =====
    cursor.execute("""
        SELECT id FROM models 
        WHERE model_name = ? AND (series_id = ? OR (series_id IS NULL AND ? IS NULL))
    """, (model_name, series_id, series_id))
    existing = cursor.fetchone()

    if existing:
        raise ValueError(f"⚠️ Model '{model_name}' already exists for this series.")

    # ===== Insert Model =====
    cursor.execute("""
        INSERT OR IGNORE INTO models (model_name, hp, series_id, tech_id, type_id)
        VALUES (?, ?, ?, ?, ?)
    """, (model_name, hp, series_id, tech_id, type_id))

    conn.commit()

def insert_ac_data(ac_data):
    for ac_type, techs in ac_data.items():
        for tech, brands in techs.items():
            for brand, series_dict in brands.items():
                for series, models in series_dict.items():
                    for model_name, hp in models.items():
                        if not model_name or not str(model_name).strip():
                            print(f"⚠️ Skipping entry with missing model name under {ac_type} → {tech} → {brand} → {series}")
                            continue
                        insert_model(ac_type, tech, brand, series, model_name, hp)

def get_ac_types():
    cursor.execute("SELECT type_name FROM ac_types")
    return [row[0] for row in cursor.fetchall()]

def get_technologies(type_name=None):
    if type_name:
        normalized = type_name.replace(" ", "_").upper()
        cursor.execute("""
            SELECT DISTINCT t.tech_name 
            FROM models m
            JOIN technology t ON m.tech_id = t.id
            JOIN ac_types a ON m.type_id = a.id
            WHERE UPPER(a.type_name) = ?
        """, (normalized,))
    else:
        cursor.execute("SELECT tech_name FROM technology")
    return [row[0] for row in cursor.fetchall()]


def get_brands(type_name=None, tech_name=None):
    query = """
        SELECT DISTINCT b.brand_name
        FROM models m
        JOIN series s ON m.series_id = s.id
        JOIN brands b ON s.brand_id = b.id
        JOIN technology t ON m.tech_id = t.id
        JOIN ac_types a ON m.type_id = a.id
        WHERE 1=1
    """

    params = []
    if type_name:
        query += " AND a.type_name = ?"
        params.append(type_name)
    if tech_name:
        query += " AND t.tech_name = ?"
        params.append(tech_name)

    cursor.execute(query, params)
    return [row[0] for row in cursor.fetchall()]

def get_series(brand, tech_name=None, type_name=None):
    query = """
        SELECT DISTINCT s.series_name
        FROM models m
        JOIN series s ON m.series_id = s.id
        JOIN brands b ON s.brand_id = b.id
        JOIN technology t ON m.tech_id = t.id
        JOIN ac_types a ON m.type_id = a.id
        WHERE b.brand_name = ?
    """
    params = [brand]
    if type_name:
        query += " AND a.type_name = ?"
        params.append(type_name)
    if tech_name:
        query += " AND t.tech_name = ?"
        params.append(tech_name)

    cursor.execute(query, params)
    return [row[0] for row in cursor.fetchall()]

def get_models(series, brand):
    cursor.execute("""
        SELECT DISTINCT m.model_name
        FROM models m
        JOIN series s ON m.series_id = s.id
        JOIN brands b ON s.brand_id = b.id
        WHERE s.series_name = ? AND b.brand_name = ?
    """, (series, brand))
    return [row[0] for row in cursor.fetchall()]

def get_hp(model_name):
    cursor.execute("SELECT hp FROM models WHERE model_name = ?", (model_name,))
    result = cursor.fetchone()
    return result[0] if result else None



# ==============================
# 🔴 DELETE FUNCTIONS
# ==============================

def delete_ac_type(type_name: str):
    type_name = type_name.replace(" ", "_").upper().strip()
    cursor.execute("SELECT id FROM ac_types WHERE type_name = ?", (type_name,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"❌ AC Type '{type_name}' not found.")
    type_id = row[0]

    # Check if models exist under this type
    cursor.execute("SELECT COUNT(*) FROM models WHERE type_id = ?", (type_id,))
    if cursor.fetchone()[0] > 0:
        raise ValueError(f"⚠️ Cannot delete AC Type '{type_name}', models are linked to it.")

    cursor.execute("DELETE FROM ac_types WHERE id = ?", (type_id,))
    conn.commit()
    return f"✅ Deleted AC Type: {type_name}"


def delete_technology(tech_name: str):
    tech_name = tech_name.upper().strip()
    cursor.execute("SELECT id FROM technology WHERE tech_name = ?", (tech_name,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"❌ Technology '{tech_name}' not found.")
    tech_id = row[0]

    cursor.execute("SELECT COUNT(*) FROM models WHERE tech_id = ?", (tech_id,))
    if cursor.fetchone()[0] > 0:
        raise ValueError(f"⚠️ Cannot delete Technology '{tech_name}', models are linked to it.")

    cursor.execute("DELETE FROM technology WHERE id = ?", (tech_id,))
    conn.commit()
    return f"✅ Deleted Technology: {tech_name}"


def delete_brand(brand_name: str):
    brand_name = brand_name.upper().strip()
    cursor.execute("SELECT id FROM brands WHERE brand_name = ?", (brand_name,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"❌ Brand '{brand_name}' not found.")
    brand_id = row[0]

    # Check if models exist for any series under this brand
    cursor.execute("""
        SELECT COUNT(*) 
        FROM series s
        JOIN models m ON m.series_id = s.id
        WHERE s.brand_id = ?
    """, (brand_id,))
    if cursor.fetchone()[0] > 0:
        raise ValueError(f"⚠️ Cannot delete Brand '{brand_name}', models are linked to its series.")

    cursor.execute("DELETE FROM series WHERE brand_id = ?", (brand_id,))
    cursor.execute("DELETE FROM brands WHERE id = ?", (brand_id,))
    conn.commit()
    return f"✅ Deleted Brand: {brand_name}"


def delete_series(series_name: str, brand_name: str):
    series_name = series_name.upper().strip()
    brand_name = brand_name.upper().strip()
    cursor.execute("""
        SELECT s.id
        FROM series s
        JOIN brands b ON s.brand_id = b.id
        WHERE s.series_name = ? AND b.brand_name = ?
    """, (series_name, brand_name))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"❌ Series '{series_name}' under '{brand_name}' not found.")
    series_id = row[0]

    cursor.execute("SELECT COUNT(*) FROM models WHERE series_id = ?", (series_id,))
    if cursor.fetchone()[0] > 0:
        raise ValueError(f"⚠️ Cannot delete Series '{series_name}', models are linked to it.")

    cursor.execute("DELETE FROM series WHERE id = ?", (series_id,))
    conn.commit()
    return f"✅ Deleted Series: {series_name}"


def delete_model(model_name: str):
    model_name = model_name.upper().strip()
    cursor.execute("SELECT id FROM models WHERE model_name = ?", (model_name,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"❌ Model '{model_name}' not found.")
    cursor.execute("DELETE FROM models WHERE id = ?", (row[0],))
    conn.commit()
    return f"✅ Deleted Model: {model_name}"


# ==============================
# ➕ APPEND HELPER FUNCTIONS
# ==============================

def add_ac_type(type_name: str):
    type_name = type_name.replace(" ", "_").upper().strip()
    cursor.execute("INSERT OR IGNORE INTO ac_types (type_name) VALUES (?)", (type_name,))
    conn.commit()
    return f"✅ Added AC Type: {type_name}"


def add_technology(tech_name: str):
    tech_name = tech_name.upper().strip()
    cursor.execute("INSERT OR IGNORE INTO technology (tech_name) VALUES (?)", (tech_name,))
    conn.commit()
    return f"✅ Added Technology: {tech_name}"


def add_brand(brand_name: str):
    brand_name = brand_name.upper().strip()
    cursor.execute("INSERT OR IGNORE INTO brands (brand_name) VALUES (?)", (brand_name,))
    conn.commit()
    return f"✅ Added Brand: {brand_name}"

def add_series(series_name: str, brand_name: str, type_name: str):
    series_name = series_name.upper().strip()
    brand_name = brand_name.upper().strip()
    type_name = type_name.replace(" ", "_").upper().strip()

    cursor.execute("SELECT id FROM brands WHERE brand_name = ?", (brand_name,))
    brand_row = cursor.fetchone()
    if not brand_row:
        raise ValueError(f"❌ Brand '{brand_name}' must exist before adding series.")
    brand_id = brand_row[0]

    cursor.execute("SELECT id FROM ac_types WHERE type_name = ?", (type_name,))
    type_row = cursor.fetchone()
    if not type_row:
        raise ValueError(f"❌ AC Type '{type_name}' must exist before adding series.")
    type_id = type_row[0]

    cursor.execute("""
        INSERT OR IGNORE INTO series (series_name, brand_id, type_id)
        VALUES (?, ?, ?)
    """, (series_name, brand_id, type_id))

    conn.commit()
    return f"✅ Added Series '{series_name}' under Brand '{brand_name}' and Type '{type_name}'"























global ac_types
ac_types = {
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
            "OTHER": {
                "": {"": ""}
            }
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
            "OTHER": {
                "": {"": ""}
            }
        },
    },
    "WALL_MOUNTED": {
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
                "DUAL INVERTER": {"LA100AE2": 1.0, "LA130AE2": 1.5},
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
            "OTHER": {
                "": {"": ""}
            }
        },

        "NON_INVERTER": {
            "KOPPEL": {
                "EVO": {"KSW-09R4A2 / KPC-09HH4A2": 1.0, "KSW-12R4A2 / KPC-12HH4A2": 1.5, "KSW-18R4A2 / KPC-18HH4A2": 2.0, "KSW-24R4A2 / KPC-24HH4A2": 2.5}
            },
            "OTHER": {
                "": {"": ""}
            }
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
            "OTHER": {
                "": {"": ""}
            }
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
            "OTHER": {
                "": {"": ""}
            }
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
            "OTHER": {
                "": {"": 1.0}
            }
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
            "OTHER": {
                "": {"": ""}
            }
        },
    },
}


# insert_ac_data(ac_types)
# print("Database populated successfully 🎉")

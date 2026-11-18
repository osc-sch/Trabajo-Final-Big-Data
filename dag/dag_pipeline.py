import pandas as pd
import duckdb
from pathlib import Path
from transform import transform
from airflow.sdk import task, dag
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"/ "rrhh.sqlite"
DB_PATH = BASE_DIR / "rrhh.duckdb"
OUTPUT_DIR = BASE_DIR / "outputs"
SQL_DIR = BASE_DIR / "SQL"

def read_sql(fielname: str):
    try:
        path = SQL_DIR / fielname
        return path.read_text(encoding="utf-8")
    except Exception as e:
        print ("Error al leer el sql: ",str(e))
        return None

def count(table_name: str,con):
    try:
        return con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchall()
    except Exception as e:
        print(f"Hubo un error al ejecutar el count ",str(e))

@task
def extract():
    conn = duckdb.connect(str(DB_PATH))
    conn.execute(f"ATTACH OR REPLACE '{str(DATA_DIR)}' AS sqlite_conn (TYPE SQLITE, READ_ONLY);")

    print("####### Extraccion #######")

    conn.execute(read_sql("extract.sql"))

    print(f"Valores Extraidos: ",count(table_name="rrhh_raw",con=conn))

@task
def validate():
    conn = duckdb.connect(str(DB_PATH))
    print("####### Validacion #######")

    conn.execute(read_sql("validations.sql"))

    print(f"Valores Validados: ",count(table_name="rrhh_validos",con=conn))
    print(f"Valores Invalidos: ",count(table_name="rrhh_rechazados",con=conn))

@task
def transformation():
    conn = duckdb.connect(str(DB_PATH))

    try:
        print("####### Transformacion #######")

        df_final = transform(conn)

        conn.register("df_temporal", df_final)

        conn.execute("""
            CREATE OR REPLACE TABLE empleados_finales AS
            SELECT * FROM df_temporal
        """)

        conn.unregister("df_temporal")

        print("Valores Transformados:", len(df_final))

    finally:
        conn.close()

@task
def export():
    conn = duckdb.connect(str(DB_PATH))

    try:
        print("####### Carga #######")

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        df_rrhh = conn.execute(
            "SELECT * FROM empleados_finales"
        ).df()

        df_rrhh.to_parquet(
            OUTPUT_DIR / "rrhh_final.parquet",
            index=False
        )

        print("Valores Exportados:", len(df_rrhh))

    finally:
        conn.close()

@dag(
    dag_id="rrhh_dag",
    start_date=datetime(2026, 11, 17),
    schedule="0 8 * * *"
)
def pipeline():

    ext = extract()
    val = validate()
    tras = transformation()
    exp = export()

    ext >> val >> tras >> exp


pipeline()
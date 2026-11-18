import pandas as pd

def completar_email(df):
    email_nulos = df["email"].isna()

    # Extraer el número del empleado
    numero_empleado = (df["id_empleado"].str.extract(r"(\d+)$", expand=False).astype(int).astype(str))

    email_generados = (df["nombre"].str.strip().str.lower()+"."+df["apellido"].str.strip().str.lower()+numero_empleado+"@tecnosur.com")

    df.loc[email_nulos,"email"] = email_generados.loc[email_nulos]

    return df

def completar_departametos(df):
    departamentos = {
        "desarrollador": "Tecnologia",
        "analista de datos": "Tecnologia",
        "soporte tecnico": "Tecnologia",
        "contador": "Finanzas",
        "tesorero": "Finanzas",
        "ejecutivo de cuentas": "Comercial",
        "vendedor": "Comercial",
        "reclutador": "RRHH",
        "generalista": "RRHH"
    }

    departamentos_nulos = df["departamento"].isna()

    departamentos_generados = df["cargo"].str.strip().str.lower().map(departamentos)

    df.loc[departamentos_nulos,"departamento"] = departamentos_generados.loc[departamentos_nulos]
    return df 

def corregir_salarios(df):
    salarios_negativos = df[df["salario"].astype(float) <= 0]

    salarios_negativos["salario"] = salarios_negativos["salario"].abs()

    df.loc[salarios_negativos.index, "salario"] = salarios_negativos["salario"]

    return df

def coregir_nombre_apellidos(df):
    df["nombre"] = df["nombre"].str.strip().str.capitalize()
    df["apellido"] = df["apellido"].str.strip().str.capitalize()

    return df


def transform(conn):
    df_rechazados = conn.sql("select * from rrhh_rechazados").df()
    df_validos = conn.sql("select * from rrhh_validos").df()

    df_rechazados = coregir_nombre_apellidos(df_rechazados)
    df_validos = coregir_nombre_apellidos(df_validos)

    df_rechazados = completar_email(df_rechazados)
    df_rechazados = completar_departametos(df_rechazados)

    df_rechazados = corregir_salarios(df_rechazados)

    df_rechazados = df_rechazados.drop(columns=["motivo_rechazo"])

    conn.execute("CREATE OR REPLACE TABLE rrhh_transformados AS SELECT * FROM df_rechazados")

    df_corregidos = pd.concat([df_validos, df_rechazados], ignore_index=True)

    print("Valores Duplicados eliminados",df_corregidos.duplicated().sum())

    df_corregidos = df_corregidos.drop_duplicates(subset=['id_empleado'])

    return df_corregidos
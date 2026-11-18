import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import pandas as pd
    import sqlite3

    conexion = sqlite3.connect("./data/rrhh.sqlite")

    tabla = pd.read_sql_query(
        "SELECT * FROM empleados",
        conexion
    )
    return pd, tabla


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Analisi de la tabla:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Informacion de la tabla:
    """)
    return


@app.cell
def _(tabla):
    tabla.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cantidad de datos NaN por columna:
    """)
    return


@app.cell
def _(tabla):
    tabla.isna().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Como se ve en los resultados tanto como en la columna de email y departamento se presenta una gran cantidad de registro con estos campos vacios, en total **313** campos vacios
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Registros duplicados:
    """)
    return


@app.cell
def _(tabla):
    cantidad_duplicados = tabla["id_empleado"].duplicated().sum()
    print(f"La cantidad de registros duplicados es de {cantidad_duplicados} registros")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Salarios Negativos
    """)
    return


@app.cell
def _(tabla):
    salarios_negativos = tabla[tabla["salario"] <= 0]
    cantidad_salario_negativo = salarios_negativos["id_empleado"].count()
    print(f"La cantidad de registros de salario negativo es de {cantidad_salario_negativo} registros")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Departamentos
    """)
    return


@app.cell
def _(tabla):
    tabla["departamento"].unique()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cargo
    """)
    return


@app.cell
def _(tabla):
    tabla["cargo"].unique()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Modalidad
    """)
    return


@app.cell
def _(tabla):
    tabla["modalidad"].unique()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Fechas
    """)
    return


@app.cell
def _(pd, tabla):
    fechas = tabla
    fechas["fecha_ingreso"] = pd.to_datetime(fechas["fecha_ingreso"], format="mixed", errors="coerce")
    cantidad_fechas_invalidas = fechas["fecha_ingreso"].isna().sum()

    if cantidad_fechas_invalidas > 0:
        print(f"La cantidad de fechas invalidas es de {cantidad_fechas_invalidas}")
    else:
        print("No hay errores al transformar las fechas, los datos son correctos")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    en este caso esta pequeña transformacion sirve para saber si hay fechas en un formato que no esta permitidos.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reglas de negocio:

    El quipo decidio optar por las siguientes reglas:
    1. **nombre**: sin espacios al principio ni al final, la primera letra Mayuscula y el resto Minusculas
    2. **apellido**: sin espacios al principio ni al final, la primera letra Mayuscula y el resto Minusculas
    3. **email**: la empresa le asigna uno, y tiene el siguiente formato "nombre"."apellido"+"numero de empleado"@tecnosur.com
    4. **fecha_ingreso**: debe contar con por lo menos uno de estos formatos para su correcta trasformacion: "25/04/2019" o "2019-04-25"
    5. **departamento**: Solo pueden estar los departamento que establece la empresa:'Tecnologia', 'Finanzas','Comercial', 'RRHH'
    6. **cargo**: solo se aceptarab los cargos que establece la empresa: 'Soporte tecnico' , 'Contador', 'Analista de datos' , 'Ejecutivo de cuentas' , 'Tesorero' , 'Desarrollador' , 'Reclutador' , 'Vendedor' , 'Generalista'. Se tomaran en cueta los cargos para completar los departamentos faltantes.
    7. **salario**: no se permitiran salarios negativos
    8. **modalidad**: solo se permitiran las siguientes modalidades: 'hibrido', 'remoto', 'presencial'
    """)
    return


@app.cell
def _():
    import duckdb

    DATABASE_URL = "rrhh.duckdb"
    engine = duckdb.connect(DATABASE_URL, read_only=False)
    return (engine,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 💼 Preguntas de negocio

    1. ¿Cual es el salario promedio por departamento?

    2. ¿Cuanto es la masa salarial total de la empresa?

    3. ¿Cuantos empleados hay por modalidad de trabajo?

    4. ¿Cuantos empleados ingresaron por año?

    5. ¿Cuales son los 3 cargos con mejor salario promedio?
    """)
    return


@app.cell
def _(engine, mo, rrhh_final):
    _df = mo.sql(
        f"""
        --1. ¿Cual es el salario promedio por departamento?
        SELECT departamento,
               ROUND(AVG(CAST(salario AS DOUBLE)), 2) AS salario_promedio
        FROM rrhh_final
        GROUP BY departamento
        ORDER BY salario_promedio DESC;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, rrhh_final):
    _df = mo.sql(
        f"""
        --2. ¿Cuanto es la masa salarial total de la empresa?
        SELECT SUM(CAST(salario AS DOUBLE)) AS masa_salarial_total
        FROM rrhh_final;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, rrhh_final):
    _df = mo.sql(
        f"""
        --3. ¿Cuantos empleados hay por modalidad de trabajo?
        SELECT modalidad,
               COUNT(*) AS cantidad_empleados
        FROM rrhh_final
        GROUP BY modalidad
        ORDER BY cantidad_empleados DESC;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, rrhh_final):
    _df = mo.sql(
        f"""
        --4. ¿Cuantos empleados ingresaron por año?
        SELECT EXTRACT(year FROM TRY_STRPTIME(CAST(fecha_ingreso AS VARCHAR),
                                              ['%d/%m/%Y', '%Y-%m-%d'])) AS anio,
               COUNT(*) AS ingresos
        FROM rrhh_final
        GROUP BY anio
        ORDER BY anio;
        """,
        engine=engine
    )
    return


@app.cell
def _(engine, mo, rrhh_final):
    _df = mo.sql(
        f"""
        --5 .¿Cuales son los 3 cargos con mejor salario promedio?
        SELECT cargo,
               ROUND(AVG(CAST(salario AS DOUBLE)), 2) AS salario_promedio
        FROM rrhh_final
        GROUP BY cargo
        ORDER BY salario_promedio DESC
        LIMIT 3;
        """,
        engine=engine
    )
    return


if __name__ == "__main__":
    app.run()

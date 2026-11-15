# 🗄️ Informe Trabajo Final Big Data

En este archivo se redacta un informe breve sobre lo que fue el desarrollo del Trabajo Final de la materia Big Data.

## 📈 Análisis

Se realizó un análisis para tener conocimientos sobre la tabla que se iba a trabajar y los tipos de datos para un mejor manejo del mismo y lograr un trabajo más eficiente.


* **Información de la tabla:** Se ejecutó el siguiente comando para tener un panorama general de la tabla y tipos de datos: 

```python
tabla.info()
```


* **Cantidad de datos NaN por columna:** Luego se queria saber cuantas columnas contaban con datos nulos por lo que se ejecutó un comado para saberlo: 

```python 
tabla.isna().sum()
```

* **Registros duplicados:** Luego se queria saber cuantas columnas contaban con datos nulos por lo que se ejecutó un comado para saberlo: 
```python
cantidad_duplicados = tabla['id_empleado'].duplicated().sum()
print(f"La cantidad de registros duplicados es de {cantidad_duplicados} registros")
```

* **Salarios Negativos:** Se queria tener conocimiento de si existian salarios negativos, es decir menores a 0, algo que no es posible, por lo tanto se realizó una consulta para averiguarlo: 

```python
salarios_negativos = tabla[tabla["salario"] <= 0]
cantidad_salario_negativo = salarios_negativos["id_empleado"].count()
print(f"La cantidad de registros de salario negativo es de {cantidad_salario_negativo} registros")
```

* **Departamentos:** Se queria tener conocimiento sobre la cantidad de departamentos existentes en la tabla por lo que se realizó la siguiente consulta: 

```python
tabla["departamento"].unique()
```

* **Cargo:** Se queria tener conocimiento sobre la cantidad de cargos existentes, por lo que se realizó la siguiente consulta: 

```python
tabla["modalidad"].unique()
```
* **Fechas:** En este caso se queria realizar una consulta para saber si existian fechas que estaban en un formato no permitido por lo que se realizó una pequeña transformación: 

```python
fechas = tabla
fechas["fecha_ingreso"] = pd.to_datetime(fechas["fecha_ingreso"], format="mixed", errors="coerce")
cantidad_fechas_invalidas = fechas["fecha_ingreso"].isna().sum()

if cantidad_fechas_invalidas > 0:
    print(f"La cantidad de fechas invalidas es de {cantidad_fechas_invalidas}")
else:
    print("No hay errores al transformar las fechas, los datos son correctos")
```
Si existía algún tipo de error se guardaria y se mostraría un mensaje detallando cuantos existían

## 📋 Reglas de negocio

El equipo decidió establecer las siguientes reglas de validación y limpieza para los datos:

1. **`nombre`:** Sin espacios al principio ni al final, con la primera letra en mayúscula y el resto en minúsculas (formato título).
2. **`apellido`:** Sin espacios al principio ni al final, con la primera letra en mayúscula y el resto en minúsculas (formato título).
3. **`email`:** Asignado por la empresa siguiendo el formato exacto `nombre.apellido+numero_empleado@tecnosur.com`.
4. **`fecha_ingreso`:** Debe cumplir con alguno de los siguientes formatos para su correcta transformación: `25/04/2019` (`DD/MM/AAAA`) o `2019-04-25` (`AAAA-MM-DD`).
5. **`departamento`:** Solo se aceptan los valores establecidos por la empresa: `Tecnología`, `Finanzas`, `Comercial` y `RRHH`.
6. **`cargo`:** Solo se permiten los siguientes cargos oficiales: `Soporte técnico`, `Contador`, `Analista de datos`, `Ejecutivo de cuentas`, `Tesorero`, `Desarrollador`, `Reclutador`, `Vendedor` y `Generalista`. *(Nota: Se utilizará el cargo como referencia para completar los departamentos faltantes).*
7. **`salario`:** No se permitirán valores negativos (menores a `0`).
8. **`modalidad`:** Solo se admiten tres opciones válidas: `híbrido`, `remoto` o `presencial`.

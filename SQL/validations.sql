
CREATE OR REPLACE TABLE rrhh_rechazados AS
SELECT *,CONCAT_WS(' | ',
        CASE
            WHEN nombre IS NULL OR TRIM(nombre) = ''
            THEN 'Nombre nulo o vacio'
        END,

        CASE
            WHEN apellido IS NULL OR TRIM(apellido) = ''
            THEN 'Apellido nulo o vacio'
        END,

        CASE
            WHEN email IS NULL OR TRIM(email) = ''
            THEN 'Email nulo o vacio'
        END,

        CASE
            WHEN TRY_STRPTIME(CAST(fecha_ingreso AS VARCHAR),['%d/%m/%Y', '%Y-%m-%d']) IS NULL
            THEN 'Fecha de ingreso nula o invalida'
        END,

        CASE
            WHEN departamento IS NULL OR TRIM(departamento) = ''
            THEN 'Departamento nulo o vacio'
            WHEN LOWER(TRIM(departamento)) NOT IN (
                'tecnologia',
                'finanzas',
                'comercial',
                'rrhh'
            )
            THEN 'Departamento invalido'
        END,

        CASE
            WHEN cargo IS NULL OR TRIM(cargo) = ''
            THEN 'Cargo nulo o vacio'
            WHEN LOWER(TRIM(cargo)) NOT IN (
                'soporte tecnico',
                'contador',
                'analista de datos',
                'ejecutivo de cuentas',
                'tesorero',
                'desarrollador',
                'reclutador',
                'vendedor',
                'generalista'
            )
            THEN 'Cargo invalido'
        END,

        CASE
            WHEN salario IS NULL OR salario <= 0
            THEN 'Salario nulo o invalido'
        END,

        CASE
            WHEN modalidad IS NULL OR TRIM(modalidad) = ''
            THEN 'Modalidad nula o vacia'
            WHEN LOWER(TRIM(modalidad)) NOT IN (
                'hibrido',
                'remoto',
                'presencial'
            )
            THEN 'Modalidad invalida'
        END

    ) AS motivo_rechazo
FROM rrhh_raw
WHERE
    nombre IS NULL OR TRIM(nombre) = ''
    OR apellido IS NULL OR TRIM(apellido) = ''
    OR email IS NULL OR TRIM(email) = ''
    OR TRY_STRPTIME(CAST(fecha_ingreso AS VARCHAR),['%d/%m/%Y', '%Y-%m-%d']) IS NULL
    OR departamento IS NULL
    OR TRIM(departamento) = ''
    OR LOWER(TRIM(departamento)) NOT IN (
        'tecnologia',
        'finanzas',
        'comercial',
        'rrhh'
    )
    OR cargo IS NULL
    OR TRIM(cargo) = ''
    OR LOWER(TRIM(cargo)) NOT IN (
        'soporte tecnico',
        'contador',
        'analista de datos',
        'ejecutivo de cuentas',
        'tesorero',
        'desarrollador',
        'reclutador',
        'vendedor',
        'generalista'
    )
    OR salario IS NULL OR salario <= 0
    OR modalidad IS NULL
    OR TRIM(modalidad) = ''
    OR LOWER(TRIM(modalidad)) NOT IN (
        'hibrido',
        'remoto',
        'presencial'
    );


CREATE OR REPLACE TABLE rrhh_validos AS
SELECT *
FROM rrhh_raw
WHERE
    nombre IS NOT NULL AND TRIM(nombre) <> ''
    AND apellido IS NOT NULL AND TRIM(apellido) <> ''
    AND email IS NOT NULL AND TRIM(email) <> ''

    AND TRY_STRPTIME(
        CAST(fecha_ingreso AS VARCHAR),
        ['%d/%m/%Y', '%Y-%m-%d']
    ) IS NOT NULL

    AND departamento IS NOT NULL
    AND TRIM(departamento) <> ''
    AND LOWER(TRIM(departamento)) IN (
        'tecnologia',
        'finanzas',
        'comercial',
        'rrhh'
    )

    AND cargo IS NOT NULL
    AND TRIM(cargo) <> ''
    AND LOWER(TRIM(cargo)) IN (
        'soporte tecnico',
        'contador',
        'analista de datos',
        'ejecutivo de cuentas',
        'tesorero',
        'desarrollador',
        'reclutador',
        'vendedor',
        'generalista'
    )

    AND salario IS NOT NULL
    AND salario > 0

    AND modalidad IS NOT NULL
    AND TRIM(modalidad) <> ''
    AND LOWER(TRIM(modalidad)) IN (
        'hibrido',
        'remoto',
        'presencial'
    );
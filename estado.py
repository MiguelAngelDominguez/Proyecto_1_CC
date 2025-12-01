def calcular_estado_inicial():
    """
    Inicializa el diccionario `estado` con los indicadores clave de la empresa,
    incluyendo todos los flags y contadores que luego se referencian en
    calcular_estado_final().
    """
    empleados = 4
    costo_emp = 2000
    precio_venta = 4.5
    return {
        # Indicadores financieros y operativos
        "Caja disponible":                   50000,
        "Inventario":                        5000,
        "Pedidos por atender":               0,
        "Unidades vendidas":                 0,
        "Insumos disponibles":               50000,
        "Cantidad de empleados":             empleados,
        "EmpleadosTemporales":               0,
        "Costo por empleado":                costo_emp,
        "Sueldos por pagar ":                 empleados * costo_emp,
        "Deuda pendiente":                   20000,
        "Reputacion del mercado":            "Nivel 3",
        "Multas e indemnizaciones":          0,
        "Maquinas (total/activas/dañadas)":  "5/5/0",

        # Banderas de prohibicion y seguro
        "Prohibir Produccion":               False,
        "Prohibir Compras":                  False,
        "Prohibir Importaciones":            False,
        "Fondo emergencia":                  False,

        # Contadores y flags temporales
        "TurnosProduccionExtra":             0,
        "DemandaExtraTemporal":              0,
        "MejoraProceso":                     False,
        "BrandingActivo":                    False,
        "MantenimientoHecho":                False,
        "EcommerceActivo":                   False,
        "InventarioMesAnterior":             0,

        'TurnoEmpleadostemporales':          0,
        'IncentivosActivos':                 False,
        'ContadordeIncentivosActivos':       0,

        'Bloqueodeclima':                    False,
        'ContadordeBloqueodeclima':          0,
        # Banadera de creditos activos
        "CreditoConcedido":                  False,

        # Carta 9
        "TurnosProhibirProduccion":          0,

        #"TurnosDemandaExtra":                0,
        #"TurnosBloqueoDemanda":              0,
        "TurnosVentasExtra":                 0,
        "DemandaExtraProximoMes":            0,
        "MultiplicadorVentas":               0,
        # Carta 6
        "TurnosDemandaReducida":             0,
        # Carta 12
        "TurnosBoicot":                      0,
        "ReductorBoicot":                    1.0
    }

def calcular_estado_final(estado):
    """
    Aplica las formulas de calculo al final de cada turno (mes) en el siguiente orden:

    1) Venta automatica
       - El precio de venta se debe cargar de la función calcular_estado_inicial()
       - Vender hasta ‘Pedidos por atender’, descontar de ‘Inventario’
       - Sumar ingresos a ‘Caja disponible’
       - Incrementar ‘Unidades vendidas’
       - Descontar Pedidos por atender’
       - Si no se atiende el total de la demanda, la 'Reputacion del mercado' se reduce un nivel

    2) Actualizacion de pedidos por atender
       - Calcular la demanda del proximo mes a partir de:
         • ‘Reputacion del mercado’
         • Flags permanentes (p. ej. ‘BrandingActivo’, ‘EcommerceActivo’)
         • Incrementos temporales (‘DemandaExtraTemporal’)
       - Almacenar en ‘Pedidos por atender’
       - Fórmula para calcular pedidos nuevos es: 1,000 x (nivel de reputación)
       - Recuerde que el Branding activo aumenta la demanda en 10%
       - Recuerde que tener un e-commerce aumenta la demanda en 5,000 unidades al mes
       - Recurde que la campaña promocional aumenta la demanda en 4,000 unidades al mes
       - Recuerde que el cobranding con una marca o influencer popular ocasiona:
        • Una demanda temporal de 300,000 solo por el primer mes (luego desaparece)
        • Una demanda temporal de 150,000 solo por el segundo mes  (luego desaparece)


    3) Pago de la nomina del mes actual
       - Tomar ‘Sueldos por pagar’
       - Si ‘Caja disponible’ ≥ ‘Sueldos por pagar’:
           • Restar de ‘Caja disponible’
         Sino:
           • Calcula cuanto es lo que falta pagar (‘Sueldos por pagar’ – ‘Caja disponible’)
           • Generar deuda con el 12% de interes total.
           • Poner ‘Caja disponible’ = 0

    4) Generacion de la nomina del proximo mes
       - Calcular ‘Sueldos por pagar’ en base a la cantidad de empleados
           • No se toma en cuenta a los empleados temporales porque a ellos ya se les pago al contratarlos.

    5) Anular multas, accidentes, y demas cartas del caos
       - Esto dependera de la carta del caos que haya salido, y de los flags que tengas activos.

    6) Produccion en automatico
       - Si ‘TurnosProduccionExtra’ > 0:
         • Se produce en automatico la misma cantidad del turno anterior (sin gastar insumos).
         • No debes disminuir ‘TurnosProduccionExtra’ porque dicho valor se reduce en el punto 7)

    7) Actualizacion de flags temporales y decremento de contadores
       - Reducir en 1 las variables contadoras. Por ejemplo:
         • ‘TurnosProduccionExtra’
         • ‘DemandaExtraTemporal’
         • ‘EmpleadosTemporales’
         • Duracion de ‘MejoraProceso’, ‘BrandingActivo’, ‘MantenimientoHecho’, etc.
       - Desactivar (poner a False o 0) cualquier flag cuyo contador llegue a cero

    8) Perdida de inventario:
       - Los meses que no se produce nada, el 10% de insumos caduca.
       - Si la produccion de este mes uso menos inventario que el 10% disponible,
         entonces, el excedente caduca (hasta completar el 10% que vence).
       - Puedes apoyarte de las variables "InventarioMesAnterior" e "Inventario"
    """

    # ============================
    # 1) Venta automatica
    # ============================
    estado["Inventario"]            = estado["Inventario"]
    estado["Unidades vendidas"]     = estado["Unidades vendidas"]
    estado["Caja disponible"]       = estado["Caja disponible"]

    ## Carta 12: Boicot de clientes
    precio_venta = 4.5
    pedidos = estado["Pedidos por atender"]
    inventario = estado["Inventario"]
    #
    ventas = min(pedidos, inventario)
    # Aplicar boicot, verifica contador
    if estado["TurnosBoicot"] > 0:
        ventas = int(ventas*estado["ReductorBoicot"])
        estado["TurnosBoicot"] -= 1
        # Si el boicot ya terminó restaurar reductor
        if estado["TurnosBoicot"] == 0:
            estado["ReductorBoicot"] = 1.0
    # Asegurar que no se venda más inventario del disponible
    ventas = min(ventas, inventario)
    # Actualizar estado
    estado["Inventario"] -= ventas
    estado["Unidades vendidas"] += ventas
    estado["Caja disponible"] += ventas * precio_venta
    estado["Pedidos por atender"] -= ventas


    # ============================
    # 2) Actualizacion de pedidos por atender
    # ============================
    estado["Pedidos por atender"]   = estado["Pedidos por atender"]
    estado["Reputacion del mercado"] = estado["Reputacion del mercado"]
    # Obtener nivel de reputación
    nivel_rep = int(estado["Reputacion del mercado"].split()[-1])


    # ============================
    # 3) Pago de la nomina del mes actual
    # ============================
    estado["Sueldos por pagar"] = estado["Sueldos por pagar"]
    estado["Caja disponible"] = estado["Caja disponible"]


    # ============================
    # 4) Generacion de la nomina del proximo mes
    # ============================
    estado["Sueldos por pagar"]     = estado["Sueldos por pagar"]


    # ============================
    # 5) Anular multas, accidentes, y demas cartas del caos
    # ============================
    estado["Prohibir Produccion"]   = estado["Prohibir Produccion"]


    # ============================
    # 6) Produccion en automatico
    #    - Si ‘TurnosProduccionExtra’ > 0:
    #     • Se produce en automatico la misma cantidad del turno anterior (sin gastar insumos).
    #     • No debes disminuir ‘TurnosProduccionExtra’ porque dicho valor se reduce en el punto 7)
    # ============================
    ## Carta
    if estado['ContadordeIncentivosActivos'] == 0:
        estado['IncentivosActivos'] = False

    if estado['IncentivosActivos']: # Si incentivos activos esta en True
        # El contador disminuye cada turno
        estado['ContadordeIncentivosActivos'] = estado['ContadordeIncentivosActivos'] - 1
        estado["Inventario"] = estado["Inventario"] * 1.2
    else: # Falta modificar para quien lo use
        estado["Inventario"] = estado["Inventario"]

    ## Carta 9: Huelga por ambiente laboral
    """if not estado["Prohibir Produccion"] and estado["TurnosProduccionExtra"] > 0:
        # Se produce lo mismo que en el mes anterior
        maquinas_str = estado["Maquinas (total/activas/dañadas)"]
        partes = maquinas_str.split('/')
        maquinas_activas = int(partes[1])
        # 2000 unidades por máquina (sin gastar insumos)
        produccion_automatica = maquinas_activas * 2000
        # Actualizar inventario
        estado["Inventario"] += produccion_automatica"""


    # ============================
    # 7) Actualizacion de flags temporales y decremento de contadores
    # ============================
    estado["TurnosProduccionExtra"] = estado["TurnosProduccionExtra"]
    # Ventas extra por campaña
    if estado["TurnosVentasExtra"] > 0:
        estado["TurnosVentasExtra"] -= 1
        if estado["TurnosVentasExtra"] == 0:
            estado["MultiplicadorVentas"] = 1.0
    # Bloqueo de campañas - cartas
    if estado["TurnosBloqueoDemanda"] > 0:
        estado["TurnosBloqueoDemanda"] -= 1
    # FALTAAAAA

    ## Carta 6:
    if estado["TurnosDemandaReducida"] > 0:
        estado["TurnosDemandaReducida"] -= 1
        """if estado["TurnosDemandaReducida"] == 0:
            estado["ReductorDemanda"] = 1.0"""


    ## Carta 9: Huelga por ambiente laboral
    # TurnosProhibidos (huelga u otros bloqueos)
    if estado["TurnosProhibirProduccion"] > 0:
        estado["TurnosProhibirProduccion"] -= 1
        # Si se acaban los turnos, liberar la prohibición
        if estado["TurnosProhibirProduccion"] == 0:
            estado["Prohibir Produccion"] = False

    ## Carta 12:
    if estado["TurnosBoicot"] > 0:
        estado["TurnosBoicot"] -= 1
        if estado["TurnosBoicot"] == 0:
            estado["TurnosBoicot"] = 0
    else:
        estado["TurnosBoicot"] = 0


    # ============================
    # 8) Perdida de inventario:
    # ============================
    estado["Inventario"]            = estado["Inventario"]

    ## Carta 8 -> (modifico para rh_incentivos)
    if estado['ContadordeBloqueodeclima'] == 0:
        estado['Bloqueodeclima'] = False

    if estado['Bloqueodeclima']: # Si bloqueodeclima esta en True
        # El contador disminuye cada turno
        estado['ContadordeBloqueodeclima'] = estado['ContadordeBloqueodeclima'] - 1

    return estado

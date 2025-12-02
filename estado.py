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
        "Sueldos por pagar":                 empleados * costo_emp,
        "Deuda pendiente":                   20000,
        "Reputacion del mercado":            "Nivel 3",
        "Multas e indemnizaciones":          0,
        "Maquinas (total/activas/dañadas)":  "5/5/0",

        # Banderas de prohibicion y seguro
        "Prohibir Produccion":               False,
        "Prohibir Compras":                  False,
        "Prohibir Importaciones":            False,
        "Fondo emergencia":                  False,
        "Prohibir ventas":                   False,

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
        "TurnosBloqueoDemanda":              0,
        # Banadera de creditos activos
        "CreditoConcedido":                  False,


        #"TurnosDemandaExtra":                0,
        #"TurnosBloqueoDemanda":              0,
        "TurnosVentasExtra":                 0,
        "DemandaExtraProximoMes":            0,
        "Ventas":                            0,
        "VentasAntMes":                      0,
        # Carta 3
        'AlmacenDeLoProducidoAnteiormente':  0,
        'Carta 3':                         False,
        "TurnosBloqueoVentasCarta3":         0,
        # Carta 4
        'Incendio':                        False,
        # Carta 6
        "TurnosDemandaReducida":             0,
        # Carta 9 y Carta 22
        "TurnosProhibirProduccion": 0,
        # Carta 12
        "TurnosBoicot":                      0,
        "ReductorBoicot":                    1.0,
        # Carta 13:
        "TurnoErrorEtiqueta":                0,
        # carta 14:
        "TurnosImportaciones":               0,
        # carta 15:
        "TurnosProhibicionComprasNacionales":0,
        # carta 18:
        "TurnosPlaga":                       0,
        # carta 24:
        "TurnosBloqueoVentas":               0,
        # Carta 26:
        "TurnoCompetidorAgresivo":           0,
        # carta 28:
        "TurnosCostos":                      0,
        # Carta 30:
        "TurnosHuelga":                      0,
        # Carta 34:
        "TurnoMalDiseñoEmpaque":             0,
        #carta 37:
        "TurnosAccidente":                   0,
        #carta 40:
        "TurnosHiringFreeze":                0,
        #de acciones
        "Coeficiente de produccion":           0,
        "TurnosMantenimiento":                 0
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
    estado['Ventas'] = min(pedidos, inventario)

    if estado["Prohibir ventas"]:
        estado['Ventas'] = 0

    # Aplicar boicot, verifica contador
    if estado["TurnosBoicot"] > 0:
        estado['Ventas'] = int(estado['Ventas'] * estado["ReductorBoicot"])
        # Si el boicot ya terminó restaurar reductor
        if estado["TurnosBoicot"] == 0:
            estado["ReductorBoicot"] = 1.0

    # Actualizar estado
    estado["Inventario"] -= estado['Ventas']
    estado["Unidades vendidas"] += estado['Ventas']
    estado["Caja disponible"] += estado['Ventas'] * precio_venta
    estado["Pedidos por atender"] -= estado['Ventas']


    # ============================
    # 2) Actualizacion de pedidos por atender
    # ============================
    estado["Pedidos por atender"]   = estado["Pedidos por atender"]
    estado["Reputacion del mercado"] = estado["Reputacion del mercado"]
    # Obtener nivel de reputación

    
    # ============================
    # 3) Pago de la nomina del mes actual
    # ============================
    sueldos = estado["Sueldos por pagar"]

    if estado["Caja disponible"] >= sueldos:
        estado["Caja disponible"] -= sueldos
    else:
        deuda = sueldos - estado["Caja disponible"]
        # 12% de interés total
        estado["Deuda"] += deuda * 1.12
        estado["Caja disponible"] = 0


    # ============================
    # 4) Generacion de la nomina del proximo mes
    # ============================

    estado["Sueldos por pagar"] = estado["Cantidad de empleados"] * estado["Costo por empleado"]

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
    # Bloqueo de campañas - cartas
    if estado["TurnosBloqueoDemanda"] > 0:
        estado["TurnosBloqueoDemanda"] -= 1
        
    # FALTAAAA

    #  Carta 3:
    if estado["TurnosBloqueoVentasCarta3"] > 0 :
        estado["TurnosBloqueoVentasCarta3"] -= 1

    ## Carta 6:
    if estado["TurnosDemandaReducida"] > 0:
        estado["TurnosDemandaReducida"] -= 1


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
    
    # Cartas 13
    if estado["TurnoErrorEtiqueta"] > 0:
        estado["TurnoErrorEtiqueta"] -= 1

    # Carta 3
    if estado['Carta 3']:
        estado['Inventario'] = estado["Inventario"] - estado['AlmacenDeLoProducidoAnteiormente']
        estado["Insumos disponibles"] += 40000
        estado['Carta 3'] = False

    # Carta 15: Prohibir compras nacionales
    if estado["TurnosProhibicionComprasNacionales"] > 0:
        estado["TurnosProhibicionComprasNacionales"] -= 1
        if estado["TurnosProhibicionComprasNacionales"] == 0:
            estado["Prohibir Compras Nacionales"] = False

    # Carta 18: Plaga
    if estado["TurnosPlaga"] > 0:
        estado["TurnosPlaga"] -= 1

    # Carta 21
    if estado["TurnosProhibirProduccion"] > 0:
        estado["TurnosProhibirProduccion"] -= 1

    # Carta 24: Bloqueo logístico
    if estado["TurnosBloqueoVentas"] > 0:
        estado["TurnosBloqueoVentas"] -= 1

    # Carta 26
    if estado["TurnoCompetidorAgresivo"] > 0:
        estado["TurnoCompetidorAgresivo"] -= 1

    # Carta 28: Crisis economica
    if estado["TurnosCostos"] > 0:
        estado["TurnosCostos"] -= 1
        if estado["TurnosCostos"] == 0:
            estado["Sueldos por pagar"] = estado["Cantidad de empleados"] * estado["Costo por empleado"]

    # Cartas 30
    if estado["TurnosHuelga"] > 0:
        estado["TurnosHuelga"] -= 1

    # Carta 34
    if estado["TurnoMalDiseñoEmpaque"] > 0:
        estado["TurnoMalDiseñoEmpaque"] -= 1

    # Carta 37: Accidente
    if estado["TurnosAccidente"] > 0:
        estado["TurnosAccidente"] -= 1
        if estado["TurnosAccidente"] == 0:
            estado["Cantidad de empleados"] += 1

    # Carta 40: Hiring Freeze
    if estado["TurnosHiringFreeze"] > 0:
        estado["TurnosHiringFreeze"] -= 1

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


    #==============================================================
    # Poner bien la reputacion del mercado, por si esta en negativo
    #==============================================================
    if int(estado["Reputacion del mercado"].split(' ')[1]) < 0:
        estado["Reputacion del mercado"] = f'Nivel 0'

    if estado['Incendio']:
        estado["Inventario"] = 0

        # TODO SOBRE LOS TURNOS PONGANLOS AL FINAL
    # Carta 14: Prohibir importaciones
    if estado["TurnosImportaciones"] > 0:
        estado["TurnosImportaciones"] -= 1
        if estado["TurnosImportaciones"] == 0:
            estado["Prohibir Importaciones"] = False

    if estado["TurnosBloqueoVentasCarta3"]==0 and estado["TurnosBloqueoVentas"]==0:
        estado["Prohibir ventas"] = False
    return estado
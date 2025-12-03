# acciones.py

# ---------------- Produccion ----------------

def produccion_producir(estado):
    """
       1. Producir:
       - Si existe el flag "Prohibir Produccion" (== True), no produce nada.
           • Ademas, usted debe implementar algun mecanismo para contar cuantos turnos de la prohibicion van pasando
       - Si no hay prohibicion, cada maquina realiza lo siguiente:
           • Consume 40 000 insumos (resta de “Insumos disponibles”).
             -> solo si Insumos disponibles ≥ 40 000, caso contrario, esa maquina no produce nada
           • Añade 2,000 unidades al inventario (suma a “Inventario”).
           • Marca que la produccion se realiza por dos turnos:
               – Debe crear o incrementar “TurnosProduccionExtra” en 2,
                 para que en el siguiente turno se pueda volver a producir,
                 asi el jugador queda libre para realizar otra accion el siguiente turno.
               - La produccion extra no consume insumos, y se hace desde calcular_estado_final, punto 7
                 (ver archivo estado.py)
       - Por cada empleado adicional contratado, la produccion aumenta en 10%, sin gastar insumos.
           • Esto se debe a que los empelados introducen eficiencias en el proceso productivo
       - Todos los turnos se peude producir, es decir, las maquinas no quedan ocupadas.
           • Esto se debe a que el proceso productivo tiene diferentes fases
       - Si no hay suficientes insumos no se puede producir.
       """
    # Verificar prohibicion
    # Si la producción está prohibida, se cuenta el turno prohibido y la función termina.
    if estado["Prohibir Produccion"]:
        return estado

    #Obtenemos las maquinas activas:
    partes = estado["Maquinas (total/activas/dañadas)"].split("/")
    maquinas_activas = int(partes[1])

    #Verficiamos cuantas maquinas pueden producir:
    maquinas_que_producen = 0

    for i in range(maquinas_activas):
        if estado["Insumos disponibles"] >= 40000:
            maquinas_que_producen += 1
            estado["Insumos disponibles"] -= 40000
        else:
            break

    if maquinas_que_producen == 0:
        return estado
    #Calculamos la produccion de las maquinas que producen:
    produccion = maquinas_que_producen * 2000

    #Aplicar bonificación por empleados:
    empleados_base = 4
    empleados_totales = estado["Cantidad de empleados"] + estado["EmpleadosTemporales"]
    empleados_extra = empleados_totales - empleados_base

    if empleados_extra > 0:
        produccion = produccion * (1 + empleados_extra * 0.10)

    if estado["MejoraProceso"]:
        #Si en caso se ejecuta la accion mejorar proceso, por cada turno aplicaremos un 5% de eficiciencia:
        produccion = produccion * (1 + estado["Coeficiente de produccion"])
    #carta 37:
    if estado["TurnosAccidente"] > 0:
        produccion *= 0.5

    # Almacenamos lo anterior
    estado['AlmacenDeLoProducidoAnteiormente'] = produccion
    #modificamos el estado:
    estado["Inventario"] += produccion
    estado["TurnosProduccionExtra"] += 2

    return estado


def produccion_pedido_encargo(estado):
    """
    2. Producir por encargo:
    Aceptamos un pedido de produccion para otra fabrica,
    la cantidad producida no va al invnetario sino que se vende inmediatamente.
    - Se debe controlar que no haya prohibicion y que existan insumos.
    - Si se realiza la produccion por encargo:
        • Genera caja inmediata de S/ 50,000 (suma a “Caja disponible”).
        • Consume 10,000 insumos (resta de “Insumos disponibles”).
    - Si no se realiza:
        • No hace nada (no varia ningun campo).
    - Si no hay suficientes insumos disponibles, no se puede producir por encargo.
    """
    if estado["Prohibir Produccion"] or estado["Insumos disponibles"]<10000:
        return estado
    else:
        estado["Caja disponible"]+=50000
        estado["Insumos disponibles"]-=10000
    return estado

def produccion_mejorar_proceso(estado):
    """
    3. Mejorar proceso:
    - Aumenta permanentemente la eficiencia de todas las maquinas.
    - Se puede elegir esta opcion en diversos turnos,
      y cada vez aumentara la produccion un 5% de la produccion base.
    - Debes implementar una variable correspondiente en el diccionario de estados.
    - Una vez aumentada la eficiencia, tu decide como hacerla efectiva:
      • En la funcion calcular_estado_final, puedes aumentar la produccion despues de haber producido
      • O puedes modificar la formula de produccion_producir para que las 20,000 unidades a producir aumenten
    - Esta mejora la hacen los ingneieros de la empresa, por lo que no genera desembolso de la caja.
    """
    estado["Coeficiente de produccion"]+=0.05
    estado["MejoraProceso"]=True

    return estado

#----------------------hecho----------------------
def produccion_mantenimiento_maquinaria(estado):
    """
    4. Mantenimiento de maquinaria:
    - Repara todas las maquinas dañadas, pasandolas a activas:
        • Ten en cuenta que las Maquinas (total/activas/dañadas) estan en formato “str/str/str”.
          Es decir, separados por el simbolo de barra diagonal "/".
          - No debes cambiar la estructura de total/activas/dañadas
            porque asi esta programado el menu de Estado de la empresa.
        • Todas las Dañadas pasan a Activas (el numero de dañadas se pone a 0,
          el numero de activas aumenta en esa cantidad).
    - Reduce el riesgo de fallas futuras:
        • Fija el flag “MantenimientoHecho = True” para que la proxima carta
          de caos que dañe maquinas sea cancelada (incluyendo las fallas por mala maniobra del personal).
        • Esta accion bloque por 3 turnos el efecto de cualquier carta del caos que involucre:
          mal funcionamiento, accidentes o siniestros, bajo rendimiento, y afines.
          (siempre y cuando la Carta de Caos guarde relacion con el estado de la maquinaria).
        • Debes implementar un contador en el Estado que indique cuantos turnos quedan de proteccion.
    - Este mantenimiento lo realiza el personal de la empresa, por lo que no genera desembolso de la caja.
    """
    maquinas = estado["Maquinas (total/activas/dañadas)"].split("/")
    maquinas_danadas = int(maquinas[2])
    maquinas_activas = int(maquinas[1])

    maquinas_activas+=maquinas_danadas
    maquinas_danadas=0

    estado["Maquinas (total/activas/dañadas)"] = maquinas[0]+"/"+str(maquinas_activas)+"/"+str(maquinas_danadas)

    estado["MantenimientoHecho"] = True
    estado["TurnosMantenimiento"] = 3  #agregare esta llave al diccionario

    return estado

def produccion_comprar_nueva_maquina(estado):
    """
    5. Comprar nueva maquina:
    - Resta S/ 10 000 de “Caja disponible”.
    - Añade 1 al total de maquinas y 1 a maquinas activas:
        • Actualiza “Maquinas (total/activas/dañadas)” en formato “str/str/str”.
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, compras la maquina nueva y te haces una deuda de S/ 11,200
    """
    maquinas = estado["Maquinas (total/activas/dañadas)"].split("/")
    maquinas_totales = int(maquinas[0])
    maquinas_activas = int(maquinas[1])
    maquinas_totales += 1
    maquinas_activas += 1

    if estado["Caja disponible"]>= 10000:
        estado["Caja disponible"]-=10000

    else:
        deuda= (10000-estado["Caja disponible"]) * (1+0.12)
        estado["Deuda pendiente"]+=deuda
        estado["Caja disponible"] = 0

    estado["Maquinas (total/activas/dañadas)"]=str(maquinas_totales)+"/"+str(maquinas_activas)+"/"+maquinas[2]
    return estado

def produccion_no_hacer_nada(estado):
    """
    6. No hacer nada en el area de produccion este turno:
    - Simplemente retorna el estado sin cambios.
    """
    return estado

# ---------------- Recursos Humanos ----------------

def rh_contratar_personal_permanente(estado):
    """
    1. Contratar personal permanente:
    - Aumenta permanentemente S/ 4,000 de “Total Salarios”.
    - Aumenta “Numero de empleados” en 1.
    - Si se vuelve a ejecutar esta accion, se aumentan 4,000 mas en salarios y 1 mas en numero de empleados.
    - Se puede seguir aumentnto el personal infinitas veces.
    """
    if estado["TurnosHiringFreeze"] > 0:
        return estado

    estado["Sueldos por pagar"] = estado["Sueldos por pagar"] + 4000
    estado['Cantidad de empleados'] = estado['Cantidad de empleados'] + 1
    return estado

def rh_contratar_personal_temporal(estado):
    """
    Outsourcing temporal:
    - Paga S/ 10 000 (pago único) para sumar 4 empleados temporales sólo este turno.
    - Si no hay suficiente dinero, se financia la diferencia con un préstamo al 12% (prorrateado).
    - Registra el número de empleados temporales y los turnos que quedan.
    """
    if estado["TurnosHiringFreeze"] > 0:
        return estado

    # vemos suficiente dinero en la caja para pagar a los empleados
    if estado['Caja disponible'] < 10000:
        # si es menor entonces hacemos un prestamo con el 12% de interes (ojo que pedimos prestado lo que nos falta para contratar)
        estado['Deuda pendiente'] += (10000 - estado['Caja disponible']) * 1.12
        # ponemos a la caja a 0
        estado['Caja disponible'] = 0
    else:
        # sino, solo le restamos 10000
        estado['Caja disponible'] = estado['Caja disponible'] - 10000
    # ahora redondeamos la deuda pendiente a 2 para mas orden visual
    estado['Deuda pendiente'] = round(estado['Deuda pendiente'], 2)
    # establecemos cuantos empleados contratamos
    estado['Empleados Temporales'] = 4
    # Registrar que estos empleados duran solo este turno
    estado["TurnoEmpleadostemporales"] = 1
    return estado


def rh_implementar_incentivos(estado):
    """
    3. Implementar incentivos:
    - Gasta S/ 5 000 en bonos.
    - Puedes fijar el flag “IncentivosActivos = True” para que, en calcular_estado_final,
      el inventario producido por 5 turnos se multiplique por 1.2 (20 % extra).
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, implementas el incentivo, y te haces una deuda de S/ 5,600
    """
    # vemos suficiente dinero en la caja para pagar a los empleados

    # Se activa el contador
    estado["ContadordeIncentivosActivos"] = 5

    if estado["Caja disponible"] < 5000:
        estado['Deuda pendiente'] += (10000 - estado['Caja disponible']) * 1.12
        estado["Caja disponible"] = 0
    else:
        estado["Caja disponible"] = estado["Caja disponible"] - 5000

    estado['IncentivosActivos'] = True
    # Ahora vamos a calcular_estado_final

    estado['Deuda pendiente'] = round(estado['Deuda pendiente'], 2)
    return estado

def rh_medicion_clima(estado):
    """
    4. Medicion de clima laboral:
    - Sin costo, se hace con el personal interno de la empresa.
    - Bloquea por 5 turnos cartas del caos relacionadas con huelgas o bajo rendimiento de personal por 3 turnos.
    - También impide por 5 turnos  que los empleados cometan errores al manipular maquinaria o mercadería.
    - También impide por 5 turnos  que empleados cometan errores logísticos como etiquetado incorrecto, o diseño de empaque incorrecto.
    - También bloquea por 5 turnos  cartas del caos relacionadas a la fuga de talento.
    - En resumen, el buen clima laboral evita errores manuales por 5 turnos.
    """

    # Bloquea por 5 turnos cartas del caos relacionadas con huelgas o bajo rendimiento de personal por 3 turnos.

    # Carta 8 ->
    estado['Bloqueodeclima'] = True
    estado['ContadordeBloqueodeclima'] = 5

    return estado

def rh_capacitar_seguridad(estado):
    """
    5. Capacitar en seguridad:
    - Sin costo, la capacitacion la hace el propio personal de la empresa.
    - Bloquea por 3 turnos Cartas del Caos relacionadas a Accidentes.
    - También impide por 3 turnos cualquier robo interno, debido al aumento en seguridad.
    - También impide por 3 turnos que los empleados descarguen virus informático por error.
    """
    return estado

def rh_subir_sueldos(estado):
    """
    6. Subir sueldos:
    - Aumenta en X% el salario de todos los empleados
        • Donde X toma el valor de 10% la primera vez,
          7% la segunda vez,
          4% la tercera vez,
          1.5%, el resto de veces.
    - Bloquea por 3 turnos las cartas del caos relacionadas a las huelgas, bajo rendimiento o fuga de talento.
    """
    return estado

def rh_no_hacer_nada(estado):
    """
    7. No hacer nada en el area de Recursos Humanos este turno:
    - Retorna el estado tal cual, sin cambios.
    """
    return estado


# ---------------- Marketing ----------------

def marketing_lanzar_campania(estado):
    """
    1. Lanzar campaña de promocion:
    - Gasta S/ 8 000 de “Caja disponible”.
    - Sube “Reputacion del mercado” a “Nivel 7”
      • Si la reputacion era mayor a 7, se mantiene en el valor que tenia (no aumenta mas).
    - Añade “DemandaExtraTemporal” de +4000 unidades para el turno actual y el siguiente.
    - Aumenta nuestras ventas en 20% por dos turnos
      • Solo aumenta si existe inventario disponible para la venta.
      • Es posible vender por encima de los pedidos que teniamos (porque aparece demanda espontanea para este mismo mes).
    - Bloquea por 5 turnos los efectos de las cartas del Caos relacionados a baja demanda, baja aceptacion del producto o cancelación de pedidos.
        • Los otros efectos de dichas cartas sí se aplicarán
    - Bloquea por 5 turnos el efecyo de reputación de las cartas del caos que afecten reputación
        • Los otros efectos de dichas cartas sí se aplicarán
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, lanzas la campaña, y te haces una deuda de S/ 8,960
    """
    costo_campaña = 8000
    interes = 0.12

    # Pago o deuda de la campaña
    if estado["Caja disponible"] < costo_campaña:
        deuda = (costo_campaña - estado["Caja disponible"]) * (1 + interes)
        estado["Deuda Pendiente"] += deuda
        estado["Caja disponible"] = 0
    else:
        estado["Caja disponible"] -= costo_campaña

    # Reputación
    nivel = int(estado["Reputacion del mercado"].split()[-1])
    if nivel < 7:
        estado["Reputacion del mercado"] = "Nivel 7"

    # Demanda Extra (2 turnos)
    # Se añade hoy y el flag continúa el siguiente turno
    estado["DemandaExtraTemporal"] += 4000
    estado["TurnosDemandaExtra"] = 2

    # Ventas +20% (2 turnos)
    if estado["Inventario"] > 0:
        estado["MultiplicadorVentas"] = 1.20
        estado["TurnosVentasExtra"] = 2
    else:
        estado["MultiplicadorVentas"] = 1.0
        estado["TurnosVentasExtra"] = 0

    # Bloquear cartas (5 turnos)
    estado["TurnosBloqueoDemanda"] = 5

    """
    FALTA............
    - Añade “DemandaExtraTemporal” de +4000 unidades para el turno actual y el siguiente.
    - Aumenta nuestras ventas en 20% por dos turnos
    - Bloquea por 5 turnos
    """

    "Carta 6" "Carta 19" "Carta 33, 34, 35, 36, 3, 9, 10, 11, 17, 20, 23, 29"

    return estado

def marketing_invertir_branding(estado):
    """
    2. Invertir en branding:
    - Gasta S/ 12 000 de “Caja disponible”.
    - Sube “Reputacion del mercado” a “Nivel 8” por 5 turnos.
        • Despues de los 5 turnos, debera regresar al valor que tenia antes.
        • Si la reputacion era mayor a 8, se mantiene en el valor que tenia.
    - Puedes fijar el flag “BrandingActivo = True” para que la demanda base
      suba un 10 % en calcular_estado_final durante estos 5 turnos.
    - Bloquea por 5 turnos las cartas del Caos relacionadas a la reputacion.
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, realizas el branding, y te haces una deuda de S/ 13,440
    """
    return estado

def marketing_estudio_mercado(estado):
    """
    3. Estudio de mercado:
    - Gasta S/ 5 000 de “Caja disponible”.
    - Ajusta “Reputacion del mercado” a “Nivel 6”.
    - Bloquea las cartas de caos relacionadas con demanda por 5 turnos.
        • Incluye cancelación de pedidos
        • No aplica para productos retirados del mercado (defectuosos)
    - Durante los próximos 3 turnos, la aparición de competidores nuevos no reducirá nuestras ventas.
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, realizas el estudio de mercado, y te haces una deuda de S/ 5,600
    """
    return estado

def marketing_abrir_ecommerce(estado):
    """
    4. Abrir canal e-commerce:
    - Si “EcommerceActivo” es False:
        • Gasta S/ 20,000 de “Caja disponible”.
        • Fija “EcommerceActivo = True”.
        • Aumenta permanentemente “Pedidos por atender” en +5,000 por turno
          (se aplica en calcular_estado_final).
        • Aumenta permanentemente “Ventas” en +2,000 por turno
          (siempre y cuando exista inventario disponible para la venta).
    - Si ya existe “EcommerceActivo” True:
        • Gasta S/ 2 000 de “Caja disponible” para mantenimiento, sin aumentar la demanda.
        • Esto bloquea por 3 turnos cualquier Carta del Caos que afecte el e-comerce.
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, te haces una deuda de S/ 22,400 o S/2,240 según corresponda
    """
    return estado

def marketing_co_branding(estado):
    """
    5. Alianza co-branding con marca o influencer muy popular:
    - Gasta S/ 3000 de “Caja disponible”.
    - Añade “DemandaExtraTemporal” de +300,000 este mes y +100,000 el proximo mes.
      • Es posible que en alianzas con marcas o influencer gigantescos
        no tengamos la capacidad para producir la cantidad de demanda que se genere.
      • Esta demanda no es permanente, si no se atiende, el nivel de demanda regres aa su valor
    - Aumenta nuestras ventas en 20% por dos turnos
      (siempre y cuando exista inventario disponible para la venta).
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, realizas la alianza, y te haces una deuda de S/ 3,360
    """
    costo_alianza = 3000        # Monto que cuesta realizar la alianza
    interes = 0.12              # Interés que se aplica si se pide préstamo
    caja_disponible = estado["Caja disponible"] # Dinero actual de la empresa

    if caja_disponible < costo_alianza:
        # Si no hay dinero suficiente en caja
        # Se pide un préstamo por la parte que falta con intereses
        deuda = (costo_alianza - caja_disponible) * (1 + interes)
        # Se suma esta deuda al total pendiente
        estado["Deuda pendiente"] += deuda
        # Como se usó tod el dinero disponible, la caja queda en cero
        estado["Caja disponible"] = 0
    else:
        # Si hay dinero en caja, se descuenta el gasto de la alianza
        estado["Caja disponible"] -= costo_alianza

    # Aplicar demanda solo del mes actual
    estado["DemandaExtraTemporal"] += 300000
    # Se aplica la demanda extra para el próximo mes
    estado["DemandaExtraProximoMes"] += 100000

    # Se aplica el aumento de ventas si es que hay inventario
    if estado["Inventario"] > 0:
        estado["TurnosVentasExtra"] += 2
        estado["MultiplicadorVentas"] = 1.20
    else:
        estado["TurnosVentasExtra"] = 0
        estado["MultiplicadorVentas"] = 1.0

    return estado



def marketing_no_hacer_nada(estado):
    """
    6. No hacer nada en el area de Marketing:
    - Retorna el estado sin cambios.
    """
    return estado


# ---------------- Compras ----------------

def compras_comprar_insumos_nacionales(estado):
    """
    1. Comprar insumos nacionales:
    - Gasta S/ 10 000 de “Caja disponible”.
    - Añade 500,000 a “Insumos disponibles”.
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, compras los insumos, y te haces una deuda de S/ 11,200
    """
    if estado["Prohibir Compras Nacionales"]:
        return estado

    return estado

def compras_comprar_insumos_importados(estado):
    """
    2. Comprar insumos importados:
    - Gasta S/ 14 000 de “Caja disponible”.
    - Añade 800,000 a “Insumos disponibles”.
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, compras los insumos, y te haces una deuda de S/ 15,680
    """
    if estado["Prohibir Importaciones"]:
        return estado
    return estado

def compras_comprar_insumos_importados_premium(estado):
    """
    3. Comprar insumos premium importados:
    - Gasta S/ 25 000 de “Caja disponible”.
    - Añade 900,000 a “Insumos disponibles”.
    - Aumenta la calidad de nuestros productos y la calidad percibida
      • Esto incrementa la demanda en un 20% por 3 meses.
      • Esto incrementa las ventas en un 20% por 3 meses.
        (siempre y cuando exista inventario disponible para la venta).
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, compras los insumos, y te haces una deuda de S/ 28,000
    """
    return estado

def compras_vender_excedentes_insumos(estado):
    """
    4. Venta de excedentes de insumos:
    - Se sabe que los meses que no hay produccion, el 10% de insumos caducan.
    - Esta accion hace que vendamos ese 10%.
      Es decir, tambien perdemos el 10% de nuestros insumos,
      pero los vendemos a 0.30 centimos cada uno.
    La accion se ejecuta por 3 turnos, incluido este.
    """
    return estado

def compras_negociar_precio(estado):
    """
    5. Negociar precio con proveedores:
    - Gasta S/ 5 000 de “Caja disponible”.
    - Permanentemente, todas las compras nacionales costaran el 70% del precio.
    - Puedes fijar un flag “DescuentoCompra = True” o “DescuentoCompra = 0.7”
      •Debes idear la forma de que esto afecte a la funcion compras_comprar_insumos_nacionales.
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, haces la negociación de precios, y te haces una deuda de S/ 5,600
    """
    return estado

def compras_negociar_credito(estado: dict):
    """
    6. Negociar crédito con proveedores:
    - Gasta S/ 2 000 de “Caja disponible”.
    - Fija el flag “CreditoConcedido = True” para que el pago de mercadería
      se postergue hasta 90 días (es decir, 3 turnos).
    - El efecto es permanente; los insumos que compres se pagarán en 90 días.
    - Debes pensar una estructura de datos que nos permita saber cuántos soles
      estamos comprando a 90 días (3 turnos) y cuántos turnos le queda a cada
      cuenta por pagar. Al momento de pagar, el dinero puede salir de caja o
      aumentar la deuda.
    - Si no hay dinero, debes pedir un préstamo al 12% de interés:
        • Es decir, haces la negociación al crédito y generas una deuda de S/ 2,240.
    """

    # Verificamos que existan las <keys> en el diccionario estado
    # <keys> requeridas:
    #  - "CreditoConcedido"
    #  - "CuentasAPagarACredito"

    # El metodo setdefault garantiza que estas claves existan; si ya existen, no altera su valor.
    estado.setdefault("CreditoConcedido", False)
    estado.setdefault("CuentasAPagarACredito", [])

    # Verificamos si ya se concedió el crédito:
    #  - Si el flag es True, quiere decir que tiene un crédito activo; por lo tanto, no tiene sentido volver a hacerlo.
    #  - Si el flag es False, quiere decir que no tiene un crédito activo; procede contodo el flujo interno del if
     
    # Esto implementa el principio de IDEMPOTENCIA, es decir: hacer la misma acción
    # dos o más veces no producirá efectos adicionales después de la primera ejecución.
    if not estado["CreditoConcedido"]:
            # Monto que debe pagarse en el momento de realizar la negociación.
            COSTO_INMEDIATO = 2000.0
            # Factor que representa un préstamo con 12% de interés.
            INTERES = 1.12

            # Almacenamos los valores de las <keys> en variables, para facilitar su acceso y manipulación
            # <keys> referidas:
            #  - "Caja disponible"
            #  - "Deuda pendiente"

            # Al usar "get", aseguramos que el flujo no falle incluso si la clave no existiera.
            caja = float(estado.get("Caja disponible", 0.0))
            deuda = float(estado.get("Deuda pendiente", 0.0))

            # Verificamos que el monto de la caja disponible en ese momento sea mayor o igual al costo inmediato.
            if caja >= COSTO_INMEDIATO:
                # Caso True:
                #      Almacenamos en la <key> "Caja disponible" su nuevo valor, que será
                #      el saldo disponible menos S/ 2 000.
                estado["Caja disponible"] = caja - COSTO_INMEDIATO
            else:
                # Caso False:
                #      Almacenamos el valor 0 en la <key> "Caja disponible".
                #      La <key> "Deuda pendiente" será igual a la suma de la deuda previa
                #      y del producto del costo inmediato por el interés.
                #
                #      Esto modela una situación financiera real: la empresa avanza con la negociación,
                #      pero lo hace a costa de endeudarse.
                estado["Deuda pendiente"] = deuda + ((COSTO_INMEDIATO - caja) * INTERES)
                estado["Caja disponible"] = 0.0
            
            # Una vez realizado el gasto (o la deuda) y completada la negociación, marcamos que el crédito ha sido concedido.
            # A partir de este punto, todas las compras de insumos deberán registrarse como compras a crédito, es decir,
            # agregarse a la lista de "CuentasAPagarACredito" con una duración de 90 días (3 turnos).
            estado["CreditoConcedido"] = True
    return estado
    

def compras_no_hacer_nada(estado):
    """
    7. No hacer nada en el area de Compras:
    - Retorna el estado sin cambios.
    """
    return estado

# ---------------- Finanzas ----------------

def finanzas_pagar_proveedores(estado):
    """
    1. Pagar proveedores:
    Esta funcion esta relacionada con compras_negociar_credito.
    Aplica para compras de insumos al credito.

    Efecto:
    Pagar al contado todas las cuentas por pagar, obteniendo un descuento del 5% por pronto pago.
    - Solo aplica para compra de insumos
    - Si no tenemos deudas a 90, 60 o 30 dias, esta accion no hace nada.

    Si no hay dinero, debes pedir un préstamo al 12% de interes equivalente al total del monto a pagar.
    """
    return estado

def finanzas_pagar_deuda(estado):
    """
    2. Pagar deuda:

    a) Si “Caja disponible” ≥ 10 000 Y “Deuda pendiente” ≥ 10 000:
       - Restar 10 000 de “Caja disponible”.
       - Restar 10 000 de “Deuda pendiente”.

    b) Si “Caja disponible” ≥ 10 000 pero “Deuda pendiente” < 10 000:
       - Su deuda restante es menor a 10 000:
         • Restar de “Caja disponible” exactamente el monto de “Deuda pendiente”.
         • Poner “Deuda pendiente” = 0.

    c) Si “Caja disponible” < 10 000 Y “Deuda pendiente” > 0:
       - Solo podra pagar hasta lo que tenga en caja:
         • pago = “Caja disponible” (el total de caja).
         • Restar “pago” de “Deuda pendiente”.
         • Poner “Caja disponible” = 0.

    En cualquier otro caso (deuda = 0 o caja = 0), no se modifica nada.
    """
    return estado

def finanzas_solicitar_prestamo(estado):
    """
    3. Solicitar prestamo:
    - Pides un préstamo de S/40,000 con un interés del 6%
    - Añade S/ 40,000 a “Caja disponible”.
    - Añade S/ 42,400 a “Deuda pendiente”.
    """
    return estado


def finanzas_crear_fondo_emergencia(estado):
    """
    4. Crear fondo de emergencia:
    - Si “Caja disponible” ≥ 50 000:
        • Resta 50 000 de “Caja disponible”.
        • Fija el flag “Fondo emergencia = True”.
    - En otro caso, retorna sin cambios.
    - Debe simplementar una variable que represente tener un fondo de emergencia.
    - Esta accion bloquea diversas Cartas del Caos que involcuren gastos inesperaods (sin importar su costo)
        • Inclye el precio de mercadería perdida por robo, accidentes o siniestros
        • Incluye gastos logísticos por productos retirados del mercado o logística inversa.
    - Si no hay dinero, debes pedir un préstamo al 12% de interes
        • Es decir, adquieres el fondo de emergencia, y te haces una deuda de S/ 56,000
    """
    return estado

def finanzas_no_hacer_nada(estado):
    """
    5. No hacer nada en el area de Finanzas:
    - Retorna el estado sin cambios.
    """
    return estado

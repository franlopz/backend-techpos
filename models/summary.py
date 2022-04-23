from core.check_business_uuid import valid_uuid
from peewee import *
from .Base import BaseModel
from database import *
from datetime import date, time, datetime, timedelta


class Ticket(BaseModel):
    id = IntegerField()
    fecha = DateField()
    hora = TimeField()
    total = FloatField()
    tipo = CharField(max_length=255)
    documento = CharField(max_length=255)
    tid = IntegerField()
    puntosLealtad = CharField(max_length=255)
    correlativo = IntegerField()
    descuentoTotal = FloatField()
    propina = FloatField()
    descuentoLealtad = FloatField()
    servicioDomicilio = FloatField()
    cliente = CharField(max_length=255)
    mesa = CharField(max_length=255)
    anulado = CharField(max_length=255)
    mesero = CharField(max_length=255)
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'tickets'


class Pago(BaseModel):
    id = IntegerField()
    fecha = DateField()
    tipoPago = CharField(max_length=255)
    pago = FloatField()
    caja = CharField(max_length=255)
    hora = TimeField()
    usuario = CharField(max_length=255)
    correlativo = IntegerField()
    anulado = CharField(max_length=255)
    iva = FloatField()
    tid = IntegerField()
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'pagos'


class Producto(BaseModel):
    id = IntegerField()
    fecha = DateField()
    hora = TimeField()
    tid = IntegerField()
    producto = CharField(max_length=255)
    cantidad = FloatField()
    porcion = CharField(max_length=255)
    venta = CharField(max_length=255)
    precio = FloatField()
    companyUuid = CharField(max_length=255)

    class Meta:
        db_table = 'productos'


def get_period(start, finish):
    if start == finish:
        return str(start)
    return str(start) + " - " + str(finish)


async def get_summary(start, finish, current_user, uuid):
    if conn.is_closed():
        conn.connect()

    dataDashboard = {
        "summary": [],
        "bytype": {},
        "byhour": {},
        "bytypeporc": {},
        "bypayment": [],
        "byitem": []
    }
    
    await valid_uuid(user=current_user, uuid=uuid)

    d1 = datetime.strptime(str(start), "%Y-%m-%d")
    d2 = datetime.strptime(str(finish), "%Y-%m-%d")
    diffDays = abs((d2 - d1).days)+1
    startPreviousPeriod = d1-timedelta(days=diffDays)
    startPreviousPeriod = startPreviousPeriod.strftime("%Y-%m-%d")
    finishPreviousPeriod = d2-timedelta(days=diffDays)
    finishPreviousPeriod = finishPreviousPeriod.strftime("%Y-%m-%d")

    currentResult = (Ticket
                     .select(fn.COALESCE(fn.SUM(Ticket.total), 0).alias('Ventas'),
                             fn.COALESCE(fn.SUM(Ticket.descuentoTotal),
                                         0).alias('Descuento'),
                             fn.COALESCE(fn.SUM(Ticket.servicioDomicilio), 0).alias(
                         'Domicilio'),
                         fn.COALESCE(fn.SUM(Ticket.propina), 0).alias('Propina'))
                     .where((Ticket.fecha >= start) & (Ticket.fecha <= finish) & (Ticket.companyUuid == uuid)))

    previousPeriodResult = (Ticket
                            .select(fn.COALESCE(fn.SUM(Ticket.total), 0).alias('Ventas'),
                                    fn.COALESCE(fn.SUM(Ticket.descuentoTotal),
                                                0).alias('Descuento'),
                                    fn.COALESCE(fn.SUM(Ticket.servicioDomicilio), 0).alias(
                                'Domicilio'),
                                fn.COALESCE(fn.SUM(Ticket.propina), 0).alias('Propina'))
                            .where((Ticket.fecha >= startPreviousPeriod) & (Ticket.fecha <= finishPreviousPeriod) & (Ticket.companyUuid == uuid)))

    salesByType = list(Ticket
                       .select(Ticket.tipo.alias('tipo'),
                               fn.COALESCE(fn.SUM(Ticket.total), 0).alias('total'))
                       .group_by(Ticket.tipo)
                       .where((Ticket.fecha >= start) & (Ticket.fecha <= finish) & (Ticket.companyUuid == uuid)))

    salesByHour = list(Ticket
                       .select(fn.HOUR(Ticket.hora)
                               .alias('hora'),
                               fn.COALESCE(fn.SUM(Ticket.total), 0)
                               .alias('total'),
                               )
                       .group_by(fn.HOUR(Ticket.hora))
                       .where((Ticket.fecha >= start) & (Ticket.fecha <= finish) & (Ticket.companyUuid == uuid)))

    salesByPayment = list(Pago
                          .select(
                              Pago.tipoPago.alias('tipo'),
                              fn.COALESCE(fn.SUM(Pago.pago), 0)
                              .alias('pago'),
                              fn.COALESCE(fn.SUM(Pago.iva), 0)
                              .alias('iva'),
                          )
                          .group_by(Pago.tipoPago)
                          .where((Pago.fecha >= start) & (Pago.fecha <= finish) & (Pago.companyUuid == uuid)))

    salesByItems = list(Producto
                        .select(
                            Producto.producto.alias('producto'),
                            fn.COALESCE(fn.SUM(Producto.precio), 0)
                              .alias('precio'),
                            fn.COALESCE(fn.SUM(Producto.cantidad), 0)
                              .alias('cantidad'),
                        )
                        .group_by(Producto.producto)
                        .where((Producto.fecha >= start) & (Producto.fecha <= finish) & (Producto.companyUuid == uuid)))

    for item in salesByItems:
        dataDashboard["byitem"].append(
            {
                "producto": item.producto,
                "precio": round(item.precio, 2),
                "cantidad": round(item.cantidad, 2),
                "porcentaje": round(item.precio*100/currentResult[0].Ventas, 2)

            }
        )

    for type in salesByType:
        dataDashboard["bytype"].update(
            {str(type.tipo): str(round(type.total, 2))})
        dataDashboard["bytypeporc"].update(
            {str(type.tipo): str(round(type.total*100/currentResult[0].Ventas, 2))})

    for hour in salesByHour:
        dataDashboard["byhour"].update(
            {str(hour.hora): str(round(hour.total, 2))})

    for payment in salesByPayment:
        dataDashboard["bypayment"].append(
            {
                "tipo": payment.tipo,
                "pago": round(payment.pago, 2),
                "iva": round(payment.iva, 2)
            }
        )

    for item in ["Ventas", "Descuento", "Domicilio", "Propina"]:
        dataDashboard['summary'].append({
            "label": item,
            "period": get_period(start, finish),
            "total": round(getattr(currentResult[0], item), 2),
            "previousTotal": round(getattr(previousPeriodResult[0], item), 2),
            "previousPeriod": get_period(startPreviousPeriod, finishPreviousPeriod),
        })

    if not conn.is_closed():
        conn.close()
    return dataDashboard

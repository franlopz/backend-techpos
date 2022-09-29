from core.check_business_uuid import valid_uuid
from peewee import *
from models.payment import Pago
from models.product import Producto
from models.ticket import Ticket
from database import *
from datetime import datetime, timedelta

def get_period(start, finish):
    if start == finish:
        return str(start)
    return str(start) + " - " + str(finish)


def get_summary(start, finish, current_user, uuid):


    dataDashboard = {
        "summary": [],
        "bytype": {},
        "byhour": {},
        "bytypeporc": {},
        "bypayment": [],
        "byitem": []
    }

    valid_uuid(user=current_user, uuid=uuid)

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
                       .where(
                           (Ticket.fecha >= start) &
                           (Ticket.fecha <= finish) &
                           (Ticket.companyUuid == uuid) &
                           (Ticket.total != 0)
                       ))

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
                          .order_by(fn.SUM(Pago.pago).desc())
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
                        .order_by(fn.SUM(Producto.precio).desc())
                        .where(
                            (Producto.fecha >= start) &
                            (Producto.fecha <= finish) &
                            (Producto.companyUuid == uuid) &
                            (Producto.precio != 0)
                        ))

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


    return dataDashboard

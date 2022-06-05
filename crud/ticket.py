from database import *
from core.check_business_uuid import valid_uuid
from models.ticket import Ticket
from peewee import *

def bulk_tickets(items, current_user, uuid):


    items_to_iterate = items
    new_items = []

    valid_uuid(user=current_user, uuid=uuid)

    for item in items_to_iterate:
        temp_item = item
        temp_item['companyUuid'] = uuid
        new_items.append(temp_item)

    bulktickets = Ticket.insert_many(new_items).execute()

    return bulktickets


def list_tickets(start, finish, current_user, uuid):


    valid_uuid(user=current_user, uuid=uuid)

    listickets = list(Ticket.select().where(
        (Ticket.fecha >= start) &
        (Ticket.fecha <= finish) &
        (Ticket.companyUuid == uuid)))


    return listickets


def non_tax_report(start, finish, current_user, uuid):


    valid_uuid(user=current_user, uuid=uuid)

    data = list(Ticket
                .select(
                    Ticket.fecha.alias('date'),
                    Ticket.docTipoId.alias('type'),
                    Ticket.docId.alias('document'),
                    Ticket.numResolucion.alias('resolution'),
                    Ticket.docSerie.alias('serie'),
                    fn.MIN(Ticket.correlativo).alias(
                        'first_company_doc_number'),
                    fn.MAX(Ticket.correlativo).alias(
                        'last_company_doc_number'),
                    fn.MIN(Ticket.correlativo).alias(
                        'first_gob_doc_number'),
                    fn.MAX(Ticket.correlativo).alias(
                        'last_gob_doc_number'),
                    Ticket.maqNum.alias('machine'),
                    fn.SUM(Ticket.venEx).alias('ex_sale'),
                    fn.SUM(Ticket.venIntExNoSujProp).alias(
                        'int_ex_sale'),
                    fn.SUM(Ticket.venNoSuj).alias('non_sub_sale'),
                    fn.SUM(Ticket.venGrabLoc).alias('taxed_sale'),
                    fn.SUM(Ticket.expDenCA).alias('exp_in_ca'),
                    fn.SUM(Ticket.expFueCA).alias('exp_out_ca'),
                    fn.SUM(Ticket.expSer).alias('exp_services'),
                    fn.SUM(Ticket.venZoFra).alias('imp_zone_sale'),
                    fn.SUM(Ticket.venCueTerNoDom).alias(
                        'third_sale'),
                    fn.SUM(Ticket.venGrabLoc).alias('total'),
                    Ticket.anexoNum.alias('append'))
                .where(
                    (Ticket.fecha >= start) &
                    (Ticket.fecha <= finish) &
                    (Ticket.companyUuid == uuid) &
                    (Ticket.anexoNum == 2) &
                    (Ticket.correlativo > 0) &
                    (Ticket.anulado == ''))
                .group_by(Ticket.fecha, Ticket.docId, Ticket.docTipoId))


    return data


def tax_payer_sales(start, finish, current_user, uuid):



    valid_uuid(user=current_user, uuid=uuid)

    data = list(Ticket
                .select(
                    Ticket.fecha.alias('date'),
                    Ticket.docTipoId.alias('type'),
                    Ticket.docId.alias('document'),
                    Ticket.numResolucion.alias('resolution'),
                    Ticket.docSerie.alias('serie'),
                    Ticket.correlativo.alias('gob_doc_number'),
                    Ticket.correlativo.alias('company_doc_number'),
                    Ticket.nrc.alias('nrc'),
                    Ticket.nombre.alias('name'),
                    Ticket.venEx.alias('ex_sale'),
                    Ticket.venNoSuj.alias('non_sub_sale'),
                    Ticket.venGrabLoc.alias('taxable_sale'),
                    Ticket.tax.alias('tax'),
                    Ticket.venCueTerNoDom.alias('third_non_dom_sale'),
                    Ticket.venCueTerNoDom.alias(
                        'third_non_dom_tax_sale'),
                    Ticket.venGrabLoc.alias('total'),
                    Ticket.dui.alias('dui'),
                    Ticket.anexoNum.alias('append'))
                .where(
                    (Ticket.fecha >= start) &
                    (Ticket.fecha <= finish) &
                    (Ticket.companyUuid == uuid) &
                    (Ticket.anexoNum == 1) &
                    (Ticket.correlativo > 0) &
                    (Ticket.anulado == ''))

                )

    return data


def voided_sales(start, finish, current_user, uuid):



    valid_uuid(user=current_user, uuid=uuid)

    unique_form_void = list(Ticket.select(
        Ticket.numResolucion.alias('resolution'),
        Ticket.docTipoId.alias('type'),
        fn.MIN(Ticket.correlativo).alias(
            'first_gob_doc_number'),
        fn.MAX(Ticket.correlativo).alias(
            'last_gob_doc_number'),
        Ticket.docId.alias('document'),
        Ticket.docSerie.alias('serie'),
        fn.MIN(Ticket.correlativo).alias(
            'first_company_doc_number'),
        fn.MAX(Ticket.correlativo).alias(
            'last_company_doc_number'))
        .where(
        (Ticket.fecha >= start) &
        (Ticket.fecha <= finish) &
        (Ticket.companyUuid == uuid) &
        (Ticket.correlativo > 0) &
        (Ticket.docTipoId == 2) &
        (Ticket.anulado == 'Si'))
        .group_by(Ticket.docId, Ticket.numResolucion, Ticket.docSerie))

    sales_voided = list(Ticket.select(
        Ticket.numResolucion.alias('resolution'),
        Ticket.docTipoId.alias('type'),
        Ticket.docId.alias('document'),
        Ticket.docSerie.alias('serie'),
        fn.MIN(Ticket.correlativo).alias(
            'first_company_doc_number'),
        fn.MAX(Ticket.correlativo).alias(
            'last_company_doc_number'))
        .where(
        (Ticket.fecha >= start) &
        (Ticket.fecha <= finish) &
        (Ticket.companyUuid == uuid) &
        (Ticket.correlativo > 0) &
        (Ticket.docTipoId == 1) &
        (Ticket.anulado == 'Si'))
        .group_by(Ticket.docId, Ticket.numResolucion, Ticket.docSerie))


    return unique_form_void + sales_voided
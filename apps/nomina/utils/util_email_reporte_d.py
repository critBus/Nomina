import io
import json
from typing import List
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseServerError
from django_reportbroD.models import ReportDefinition
from reportbro import Report, ReportBroError
import os
from ..models import NOMBRE_CARGO_DIRECTOR, Trabajador
from django.utils import timezone

def custom_export_report_by_name(template_name, data, file="reporte", send_email=False):
    """Export a report using its name"""

    report = ReportDefinition.objects.filter(name=template_name).first()

    if not report:
        return HttpResponseServerError("Este reporte no se encuentra disponible")

    # if extension.lower() == "xlsx":
    #     return reportXLSX(report.report_definition, data, file)

    return customReportPDF(
        report.report_definition, data, file, send_email, template_name
    )


def customReportPDF(
    report_definition, data, file="reporte", send_email=False, nombre_reporte=None
):
    """Prints a pdf file with the available data and optionally sends it as an email attachment."""

    try:
        report_inst = Report(json.loads(report_definition), data)

        if report_inst.errors:
            raise ReportBroError(report_inst.errors[0])

        pdf_report = report_inst.generate_pdf()

        if send_email and settings.SEND_EMAIL:
            directores: List[Trabajador] = Trabajador.objects.filter(
                cargo=NOMBRE_CARGO_DIRECTOR
            )
            for director in directores:
                email_to = director.email
                if email_to:
                    subject = nombre_reporte
                    body = "Adjunto encontrarás el reporte solicitado."
                    fp = io.BytesIO(pdf_report)

                    print(f"email_to={email_to}")
                    email = EmailMessage(subject, body, to=[email_to])
                    email.attach(
                        filename="report.pdf",
                        content=fp.read(),
                        mimetype="application/pdf",
                    )
                    cantidad_enviados = email.send(fail_silently=True)
                    print(f"cantidad_enviados={cantidad_enviados}")

        response = HttpResponse(bytes(pdf_report), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="{filename}"'.format(
            filename=f"{file}.pdf"
        )

        return response
    except Exception as e:
        # Handle any exceptions or errors that may occur during the process
        print(f"An error occurred: {str(e)}")
        return HttpResponse("An error occurred while processing the report")



def load_json(filename, force=False):
    actual = timezone.now()
    file = json.load(open(filename, "r"))
    name = file["name"]
    if not ReportDefinition.objects.filter(name=name).exists():
        ReportDefinition.objects.create(
            name=name,
            report_definition=file["report_definition"],
            remark=file["remark"],
            last_modified_at=actual,
        )
        print(f"reporte cargado: {name}")
    elif force:
        ReportDefinition.objects.filter(name=name).delete()
        ReportDefinition.objects.create(
            name=name,
            report_definition=file["report_definition"],
            remark=file["remark"],
            last_modified_at=actual,
        )
        print(f"reporte cargado: {name}")


def load_report(repor_name, folder="reportes_json", force=False):
    filename = f"{repor_name}.json"
    dire = os.path.join(settings.BASE_DIR, folder)
    load_json(os.path.join(dire, filename), force=force)


def load_automatic_reports(folder="reportes_json"):
    print("cargando reportes ...")
    dire = os.path.join(settings.BASE_DIR, folder)
    for filename in os.listdir(dire):
        load_json(os.path.join(dire, filename))

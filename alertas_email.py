import smtplib
from email.message import EmailMessage

def enviar_alerta(resumen_path, destinatario="tu@email.com"):
    msg = EmailMessage()
    msg["Subject"] = "Resumen de Archivos Archivados"
    msg["From"] = "automatizacion@empresa.com"
    msg["To"] = destinatario
    msg.set_content("Adjunto el resumen de archivos archivados.")

    with open(resumen_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="resumen_archivo.xlsx")

    with smtplib.SMTP("smtp.tu-servidor.com", 587) as server:
        server.starttls()
        server.login("usuario", "contraseña")
        server.send_message(msg)
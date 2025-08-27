import os
import smtplib
from email.message import EmailMessage
from scripts.historial_archivo import registrar_evento

def enviar_alerta(resumen_path, destinatario="tu@email.com"):
    if not os.path.exists(resumen_path):
        registrar_evento("historial_archivo.xlsx", "Error al enviar alerta: resumen no encontrado")
        raise FileNotFoundError(f"❌ No se encontró el archivo de resumen: {resumen_path}")

    msg = EmailMessage()
    msg["Subject"] = "Resumen de documentos archivados"
    msg["From"] = "automatizacion@empresa.com"
    msg["To"] = destinatario
    msg.set_content("Adjunto el resumen de los documentos archivados.")

    with open(resumen_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=os.path.basename(resumen_path)
        )

    try:
        with smtplib.SMTP("smtp.tu-servidor.com", 587) as server:
            server.starttls()
            server.login("usuario", "contraseña")
            server.send_message(msg)
        registrar_evento("historial_archivo.xlsx", "Alerta enviada correctamente", resumen_path)
        print("✅ Alerta enviada correctamente")
    except Exception as e:
        registrar_evento("historial_archivo.xlsx", f"Error al enviar alerta: {str(e)}", resumen_path)
        raise RuntimeError(f"❌ Falló el envío de alerta: {str(e)}")
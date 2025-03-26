import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def generate_email_template(jobs, token=None):
    """
    Genera una plantilla HTML para correo (compatible con Outlook) a partir de una lista de empleos.
    Incluye un botón "Aplicar" en cada empleo.
    """
    # Se hace referencia al logo mediante CID; el logo se adjuntará en el envío.
    email_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FindMT</title>
</head>
<body style="margin:0; padding:0; background-color:#f4f4f4;">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td align="center" style="padding: 10px 0;">
        <table border="0" cellpadding="0" cellspacing="0" width="600" style="border: 1px solid #cccccc; background-color:#ffffff;">
          <tr>
            <td align="center" bgcolor="#ffffff" style="padding: 20px 0;">
              <img src="cid:logo_cid"  width="200" alt="Logo" style="display: block; margin: auto;">
            </td>
          </tr>
          <tr>
            <td style="padding: 40px 30px; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px; color: #333333;">
              <p>Hola,</p>
              <p>A continuación, te presentamos las oportunidades de empleo encontradas:</p>
    """
    for job in jobs:
        # Construir el enlace "Aplicar": si se obtuvo un token se incluye como parámetro adicional
        if token:
            aplicar_link = f"https://empleateya.mt.gob.do/web/candidatos/puestos?advancedSearch=1&id={job.get('id')}&access_token={token}"

        email_html += f"""
              <table border="0" cellpadding="20" cellspacing="0" width="100%" style="margin-bottom:20px; border:1px solid #e0e0e0; border-radius: 10px; background: #f8fafc;">
                <tr>
                  <td style="font-weight:bold; width:150px;">Título:</td>
                  <td>{job.get('titulo', 'No especificado')}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Descripción:</td>
                  <td>{job.get('descripcion', 'No especificado')}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Beneficios:</td>
                  <td>{job.get('beneficiosGenerales', 'No especificado')}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Requisitos:</td>
                  <td>{job.get('requisitosGenerales', 'No especificado')}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Salario:</td>
                  <td>{job.get('salario', 'No especificado')}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Cantidad:</td>
                  <td>{job.get('cantidad', 'No especificado')}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Fecha Vencimiento:</td>
                  <td style="text-decoration: none;">{job.get('fechaVencimiento', 'No especificado')}</td>
                </tr>
                <tr>
                  <td style="font-weight:bold;">Provincia:</td>
                  <td>{job.get('provincia', 'No especificado')}</td>
                </tr>
                <tr>
                  <td colspan="2" align="left" style="padding-top: 10px;">
                    <a href="{aplicar_link}" target="_blank" style="background-color:#007BFF; color:#ffffff; text-decoration:none; padding:8px 16px; border-radius:4px; font-size:14px; display:inline-block;">Aplicar</a>
                  </td>
                </tr>
              </table>
        """
    email_html += """
              <p>Saludos cordiales,</p>
              <p><strong>Equipo de FindMT</strong></p>
            </td>
          </tr>
          <tr>
            <td bgcolor="#336699" style="padding: 30px; font-family: Arial, sans-serif; font-size: 14px; color: #ffffff;">
              <p style="margin: 0;">© 2025 FindMT. Todos los derechos reservados.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return email_html

def send_email(subject, html_content, sender_email, receiver_email, smtp_server, 
               smtp_port, login, password, logo_path):
    """
    Configura y envía el correo utilizando SMTP.
    """
    message = MIMEMultipart('related')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email

    # Crear la parte "alternative" (puede contener versiones en texto y HTML)
    msg_alternative = MIMEMultipart("alternative")
    message.attach(msg_alternative)
    
    part = MIMEText(html_content, 'html')
    msg_alternative.attach(part)
    
        # Abrir y adjuntar la imagen con Content-ID "logo_cid"
    with open(logo_path, "rb") as f:
        logo_data = f.read()
    image = MIMEImage(logo_data)
    image.add_header("Content-ID", "<logo_cid>")
    image.add_header("Content-Disposition", "inline", filename="trabajo.png")
    message.attach(image)
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Activa la seguridad TLS
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Correo enviado exitosamente.")
    except Exception as e:
        print("Error al enviar correo:", e)

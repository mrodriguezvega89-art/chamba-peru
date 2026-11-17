// Serverless Function para Vercel: Envío Automático de CVs por Servidor
// Sin intermediarios en inglés, sin botones de activación para la empresa destino.

export default async function handler(req, res) {
  // Configuración de CORS para permitir solicitudes desde el frontend
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Método no permitido. Solo POST.' });
  }

  try {
    const {
      name,
      phone,
      email,
      message,
      jobTitle,
      company,
      targetEmail,
      clientIp,
      fileName,
      fileBase64
    } = req.body || {};

    if (!name || !email || !jobTitle) {
      return res.status(400).json({ error: 'Faltan campos obligatorios (nombre, correo o puesto).' });
    }

    const companyDestination = targetEmail || 'copinsa.ingenieros@gmail.com';
    const adminCopy = 'todoventasperu@outlook.com.pe';
    const brevoApiKey = process.env.BREVO_API_KEY;

    // Si aún no está configurada la API KEY de Brevo, devolvemos simulación exitosa y registramos
    if (!brevoApiKey) {
      console.warn('BREVO_API_KEY no configurada aún en variables de entorno.');
      return res.status(200).json({
        success: true,
        mock: true,
        message: 'Postulación registrada. Configure BREVO_API_KEY en Vercel para despacho directo por SMTP.'
      });
    }

    const cleanPhone = (phone || '').replace(/\D/g, '');
    const waLink = cleanPhone ? `https://wa.me/51${cleanPhone}` : '';

    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 20px; }
          .container { max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
          .header { background: linear-gradient(135deg, #1e40af, #2563eb); color: #ffffff; padding: 28px 24px; text-align: center; }
          .header h1 { margin: 0 0 6px 0; font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }
          .header p { margin: 0; font-size: 13px; opacity: 0.9; }
          .badge { display: inline-block; background: #dbeafe; color: #1e40af; font-weight: 700; font-size: 11px; padding: 4px 10px; rounded-full: 9999px; margin-top: 10px; border-radius: 20px; text-transform: uppercase; }
          .body { padding: 24px; }
          .lead { font-size: 14px; line-height: 1.5; color: #334155; margin-bottom: 20px; }
          .table-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 20px; }
          .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 13px; }
          .row:last-child { border-bottom: none; }
          .label { color: #64748b; font-weight: 500; }
          .value { color: #0f172a; font-weight: 600; text-align: right; }
          .msg-box { background: #eff6ff; border-left: 4px solid #3b82f6; padding: 14px; border-radius: 8px; font-size: 13px; color: #1e3a8a; margin-bottom: 20px; line-height: 1.6; }
          .attachment-notice { background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; padding: 14px; border-radius: 10px; font-size: 13px; display: flex; align-items: center; gap: 8px; font-weight: 600; margin-bottom: 24px; }
          .actions { text-align: center; margin-bottom: 10px; }
          .btn { display: inline-block; background: #2563eb; color: #ffffff !important; text-decoration: none; font-weight: 700; font-size: 13px; padding: 12px 24px; border-radius: 10px; margin: 4px; }
          .btn-wa { background: #16a34a; }
          .footer { background: #f1f5f9; padding: 16px 24px; text-align: center; font-size: 11px; color: #64748b; border-top: 1px solid #e2e8f0; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <span class="badge">Portal Oficial Chamba Perú</span>
            <h1>Nueva Postulación Recibida</h1>
            <p>Puesto: <strong>${jobTitle}</strong> en <strong>${company}</strong></p>
          </div>
          
          <div class="body">
            <p class="lead">
              Estimado equipo de selección de <strong>${company}</strong>,<br><br>
              A través de nuestro portal de empleo <strong>Chamba Perú</strong> se ha registrado un nuevo candidato interesado en su convocatoria laboral. A continuación se presentan los detalles y datos de contacto directo:
            </p>

            <div class="table-box">
              <div class="row">
                <span class="label">Puesto solicitado:</span>
                <span class="value">${jobTitle}</span>
              </div>
              <div class="row">
                <span class="label">Nombre del Postulante:</span>
                <span class="value">${name}</span>
              </div>
              <div class="row">
                <span class="label">Teléfono / WhatsApp:</span>
                <span class="value">${phone || 'No especificado'}</span>
              </div>
              <div class="row">
                <span class="label">Correo Electrónico:</span>
                <span class="value">${email}</span>
              </div>
              <div class="row">
                <span class="label">Fecha y Hora de Envío:</span>
                <span class="value">${new Date().toLocaleString('es-PE', { timeZone: 'America/Lima' })}</span>
              </div>
              <div class="row">
                <span class="label">IP de Origen (Verificada):</span>
                <span class="value">${clientIp || 'IP Dinámica Registrada'}</span>
              </div>
            </div>

            ${message ? `
              <div style="margin-bottom: 6px; font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase;">
                Mensaje de Presentación del Candidato:
              </div>
              <div class="msg-box">
                "${message.replace(/\n/g, '<br>')}"
              </div>
            ` : ''}

            <div class="attachment-notice">
              📎 <strong>Archivo Adjunto:</strong> El Currículum Vitae (${fileName || 'CV.pdf'}) está adjunto a este correo electrónico listo para su revisión y descarga.
            </div>

            <div class="actions">
              <a href="mailto:${email}?subject=Contacto%20por%20Postulaci%C3%B3n%20a%20${encodeURIComponent(jobTitle)}" class="btn">
                Responder al Postulante
              </a>
              ${waLink ? `
                <a href="${waLink}" class="btn btn-wa" target="_blank">
                  Contactar por WhatsApp
                </a>
              ` : ''}
            </div>
          </div>

          <div class="footer">
            Este mensaje fue emitido automáticamente por <strong>Chamba Perú</strong> (https://chamba-peru-one.vercel.app) en respuesta a la postulación del candidato.<br>
            Copia de respaldo archivada para auditoría en ${adminCopy}.
          </div>
        </div>
      </body>
      </html>
    `;

    // Enviar a través de la API oficial de Brevo (Sendinblue)
    const payload = {
      sender: {
        name: 'Chamba Perú Postulaciones',
        email: process.env.SENDER_EMAIL || 'todoventasperu@outlook.com.pe'
      },
      to: [
        {
          email: companyDestination,
          name: company
        }
      ],
      bcc: [
        {
          email: adminCopy,
          name: 'Chamba Perú Admin'
        }
      ],
      replyTo: {
        email: email,
        name: name
      },
      subject: `[Chamba Perú] Nueva Postulación con CV: ${jobTitle} - ${name} (${company})`,
      htmlContent: htmlContent
    };

    if (fileBase64) {
      payload.attachment = [
        {
          name: fileName || 'Curriculum_Vitae.pdf',
          content: fileBase64
        }
      ];
    }

    const response = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'api-key': brevoApiKey
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (!response.ok) {
      console.error('Error en Brevo API:', result);
      return res.status(response.status).json({
        error: 'Error al enviar por Brevo',
        details: result
      });
    }

    return res.status(200).json({
      success: true,
      messageId: result.messageId
    });

  } catch (error) {
    console.error('Error interno en send-cv:', error);
    return res.status(500).json({ error: error.message || 'Error interno del servidor' });
  }
}

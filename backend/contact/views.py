from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus
from .models import Contact
from utilities import utilities 
import logging


logger = logging.getLogger(__name__)

class ContactListAPIView(APIView):
    """
    API view to handle contact form submissions.
    Creates a contact record and sends a confirmation email to the user.
    """

    def post(self, request):
        required_fields = {
            "name": "nombre",
            "email": "correo electrónico",
            "phone": "teléfono",
            "message": "mensaje",
        }

        for field_key, field_display_name in required_fields.items():
            if request.data.get(field_key) is None:
                return Response(
                    {"error": f"El campo '{field_display_name}' es obligatorio."},
                    status=HTTPStatus.BAD_REQUEST
                )

        try:
            
            contact = Contact.objects.create(
                name=request.data["name"],
                email=request.data["email"],
                phone=request.data["phone"],
                message=request.data["message"]
                )


            html_content = f"""
                <h1>Confirmación de Mensaje Recibido - WebRecetas</h1>
                <p>Hola {contact.name},</p>
                <p>Hemos recibido tu mensaje y nos pondremos en contacto contigo pronto si es necesario. Aquí tienes una copia de tu consulta:</p>
                <ul>
                    <li><strong>Nombre:</strong> {contact.name}</li>
                    <li><strong>Correo:</strong> {contact.email}</li>
                    <li><strong>Teléfono:</strong> {contact.phone}</li>
                    <li><strong>Mensaje:</strong> {contact.message}</li>
                </ul>
                <p>Gracias por contactarnos.</p>
            """
            email_subject = "Confirmación de tu mensaje en WebRecetas"           
            utilities.send_mail(html_content, email_subject, contact.email)
            logger.info(f"Formulario de contacto procesado para {contact.email}. Intento de envío de correo realizado.")

            return Response({"mensaje": "Tu mensaje ha sido recibido y guardado correctamente. Hemos enviado una confirmación a tu correo."}, status=HTTPStatus.CREATED)

        except Exception as e:
            logger.error(f"Error inesperado al procesar el formulario de contacto para {request.data.get('email', 'Email no proporcionado')}: {e}", exc_info=True)
            return Response(
                {"error": "Ocurrió un error inesperado al procesar su solicitud. Por favor, inténtelo de nuevo más tarde."},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

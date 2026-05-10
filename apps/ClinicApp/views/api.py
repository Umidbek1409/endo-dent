import json
import logging
import sys
import requests
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ..models import Service, ClinicInfo, Appointment

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def submit_appointment(request):
    """
    API endpoint to handle appointment form submissions.
    """
    try:
        data = json.loads(request.body)

        full_name = data.get('full_name', '').strip()
        phone = data.get('phone', '').strip()

        if not full_name:
            return JsonResponse({'success': False, 'error': 'Full name is required'})
        if not phone:
            return JsonResponse({'success': False, 'error': 'Phone number is required'})

        # Handle preferred_date
        preferred_date = None
        date_raw = data.get('preferred_date')
        if date_raw and isinstance(date_raw, str):
            date_str = date_raw.strip()
            if date_str:
                try:
                    from datetime import datetime
                    preferred_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    preferred_date = None

        # Handle preferred_time
        preferred_time = data.get('preferred_time', '').strip()
        if not preferred_time:
            preferred_time = ''

        # Handle service
        service_obj = None
        service_id = data.get('service')
        if service_id:
            try:
                service_obj = Service.objects.get(pk=int(service_id))
            except (Service.DoesNotExist, ValueError, TypeError):
                service_obj = None

        # Handle message
        message = data.get('message', '').strip()
        if not message:
            message = ''

        # Create appointment
        try:
            appointment = Appointment.objects.create(
                full_name=full_name,
                phone=phone,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                service=service_obj,
                message=message,
            )
        except ValidationError as ve:
            print(f"VALIDATION ERROR: {ve.message_dict}", file=sys.stderr)
            return JsonResponse({'success': False, 'error': f'Validation error: {ve.message_dict}'})

        # Send Telegram notification
        try:
            clinic_info = ClinicInfo.objects.first()
            if clinic_info and clinic_info.telegram_bot_token and clinic_info.telegram_chat_id:
                service_name = service_obj.title if service_obj else '-'
                message_text = (
                    "🔔 Yangi mijoz!\n\n"
                    f"👤 Ism: {full_name}\n"
                    f"📞 Telefon: {phone}\n"
                    f"📅 Sana: {preferred_date or '-'}\n"
                    f"🕐 Vaqt: {preferred_time or '-'}\n"
                    f"🦷 Xizmat: {service_name}\n"
                    f"💬 Izoh: {message or '-'}"
                )
                url = f"https://api.telegram.org/bot{clinic_info.telegram_bot_token}/sendMessage"
                requests.post(url, json={
                    'chat_id': clinic_info.telegram_chat_id,
                    'text': message_text,
                    'parse_mode': 'HTML'
                }, timeout=5)
        except Exception as e:
            logger.warning(f"Failed to send Telegram notification: {e}")

        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request data'})
    except Exception as e:
        logger.exception("Unexpected error in submit_appointment")
        return JsonResponse({'success': False, 'error': f'Internal server error: {str(e)}'})

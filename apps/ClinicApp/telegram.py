"""
Dental Clinic - Telegram Notification Utility

Sends appointment notifications to a Telegram group/channel
using the Telegram Bot API.
"""

import logging

import requests

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def send_telegram_message(bot_token, chat_id, text, parse_mode="HTML"):
    """
    Sends a message to a Telegram group/channel.

    Args:
        bot_token: Telegram Bot Token from @BotFather
        chat_id: Group/Channel ID (e.g. '-1001234567890')
        text: Message text (supports HTML formatting)
        parse_mode: 'HTML' or 'Markdown' (default: 'HTML')

    Returns:
        True if message was sent successfully, False otherwise
    """
    if not bot_token or not chat_id:
        logger.warning("Telegram bot_token or chat_id not configured")
        return False

    url = TELEGRAM_API_URL.format(token=bot_token)
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Telegram message sent successfully to chat_id=%s", chat_id)
        return True
    except requests.RequestException as e:
        logger.error("Failed to send Telegram message: %s", str(e))
        return False


def format_appointment_message(appointment):
    """
    Formats an Appointment object into a readable HTML message for Telegram.

    Args:
        appointment: Appointment model instance

    Returns:
        Formatted HTML string
    """
    service_name = appointment.service.title if appointment.service else "Belgilanmagan"

    message = (
        f"🦷 <b>Yangi qabul arizasi!</b>\n\n"
        f"👤 <b>Ism:</b> {appointment.full_name}\n"
        f"📞 <b>Telefon:</b> {appointment.phone}\n"
        f"📧 <b>Email:</b> {appointment.email or '—'}\n"
        f"🏥 <b>Xizmat:</b> {service_name}\n"
        f"📅 <b>Sana:</b> {appointment.preferred_date}\n"
        f"🕐 <b>Vaqt:</b> {appointment.preferred_time or '—'}\n"
        f"💬 <b>Izoh:</b> {appointment.message or '—'}\n\n"
        f"🕒 <i>Yuborilgan: {appointment.submitted_at.strftime('%d.%m.%Y %H:%M')}</i>"
    )

    return message


def notify_appointment(appointment):
    """
    Sends an appointment notification to Telegram.

    Reads bot_token and chat_id from the ClinicInfo singleton model.

    Args:
        appointment: Appointment model instance

    Returns:
        True if message was sent successfully, False otherwise
    """
    from .models import ClinicInfo

    clinic_info = ClinicInfo.objects.first()

    if not clinic_info:
        logger.warning("ClinicInfo not configured")
        return False

    bot_token = clinic_info.telegram_bot_token
    chat_id = clinic_info.telegram_chat_id

    text = format_appointment_message(appointment)

    return send_telegram_message(bot_token, chat_id, text)

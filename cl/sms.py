from django.conf import settings
from twilio.rest import TwilioRestClient
#from django.template.loader import render_to_string

def send_sms(to, message):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(body=message, to=to, from_='+12015604123')
    return response
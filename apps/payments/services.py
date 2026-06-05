"""
M-Pesa Daraja API Service.
Handles STK Push initiation and access token management.
"""
import base64
import requests
import logging
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


class MpesaService:
    BASE_URL = {
        'sandbox': 'https://sandbox.safaricom.co.ke',
        'production': 'https://api.safaricom.co.ke',
    }

    def __init__(self):
        self.env = settings.MPESA_ENV
        self.base = self.BASE_URL[self.env]

    def _get_access_token(self):
        url = f'{self.base}/oauth/v1/generate?grant_type=client_credentials'
        r = requests.get(url, auth=(
            settings.MPESA_CONSUMER_KEY,
            settings.MPESA_CONSUMER_SECRET
        ))
        r.raise_for_status()
        return r.json()['access_token']

    def _generate_password(self, timestamp):
        raw = f'{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}'
        return base64.b64encode(raw.encode()).decode()

    def initiate_stk_push(self, phone: str, amount: int, account_ref: str, description: str) -> dict:
        """
        Initiate STK Push to customer phone.
        phone: '254XXXXXXXXX' format (no + prefix)
        amount: integer KSH
        Returns: {'CheckoutRequestID': ..., 'MerchantRequestID': ..., 'ResponseCode': '0', ...}
        Raises: requests.HTTPError on failure
        """
        token = self._get_access_token()
        ts = datetime.now().strftime('%Y%m%d%H%M%S')
        payload = {
            'BusinessShortCode': settings.MPESA_SHORTCODE,
            'Password': self._generate_password(ts),
            'Timestamp': ts,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone,
            'PartyB': settings.MPESA_SHORTCODE,
            'PhoneNumber': phone,
            'CallBackURL': settings.MPESA_CALLBACK_URL,
            'AccountReference': account_ref,
            'TransactionDesc': description,
        }
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.post(
            f'{self.base}/mpesa/stkpush/v1/processrequest',
            json=payload, headers=headers
        )
        r.raise_for_status()
        return r.json()

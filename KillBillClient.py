from KillBillRequestPayloads import KillBillRequestPayloads
from KillBillHttpClient import KillBillHttpClient
from KillBillTags import KillBillTags as tags
import json
import time
import logging


class KillBillClient:

    def __init__(self, host, username, password, api_key, api_secret):
        self.httpClient = KillBillHttpClient(host, username, password, api_key, api_secret)
        self.payloads = KillBillRequestPayloads()

    def create_account(self, first_name, external_key):
        payload = self.payloads.get_create_account_payload(first_name, external_key)
        response = self.httpClient.do_post('/accounts', payload)

        if response.status_code == 201:
            new_object_id = response.headers['Location'][-36:]
            logging.info('Account created id=%s, external_key=%s', new_object_id, external_key)
            return new_object_id
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return None

    def create_payment_method(self, account_id, is_default, plugin_name, cc_number, cc_cvv, cc_month, cc_year):
        payload = self.payloads.get_create_payment_method_payload(account_id, plugin_name,  cc_number, cc_cvv, cc_month, cc_year)
        response = self.httpClient.do_post('/accounts/' + account_id + '/paymentMethods?isDefault=' + is_default, payload)

        if response.status_code == 201:
            new_object_id = response.headers['Location'][-36:]
            logging.info('Payment method id=%s, card number=%s', new_object_id, cc_number)
            return new_object_id
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return None

    def create_auto_pay_off_tag(self, account_id):
        response = self.httpClient.do_post('/accounts/' + account_id + '/tags?tagList=' + tags.AUTO_PAY_OFF, None)
        status_code = response.status_code

        if status_code == 201:
            logging.info('Account %s has been tagged with AUTO_PAY_OFF(%s) ', account_id, tags.AUTO_PAY_OFF)
            return True
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return False

    def create_auto_invoicing_off_tag(self, account_id):
        response = self.httpClient.do_post('/accounts/' + account_id + '/tags?tagList=' + tags.AUTO_INVOICING_OFF, None)
        status_code = response.status_code

        if status_code == 201:
            logging.info('Account %s has been tagged with AUTO_INVOICING_OFF(%s) ', account_id, tags.AUTO_INVOICING_OFF)
            return True
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return False

    def remove_auto_pay_off_tag(self, account_id):
        response = self.httpClient.do_delete('/accounts/' + account_id + '/tags?tagList=' + tags.AUTO_PAY_OFF)
        status_code = response.status_code

        if status_code == 200:
            logging.info('Tag AUTO_PAY_OFF(%s) has been removed from %s ', tags.AUTO_PAY_OFF, account_id)
            return True
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return False

    def remove_auto_invoicing_off_tag(self, account_id):
        response = self.httpClient.do_delete('/accounts/' + account_id + '/tags?tagList=' + tags.AUTO_INVOICING_OFF)
        status_code = response.status_code

        if status_code == 200:
            logging.info('Tag AUTO_INVOICING_OFF(%s) has been removed from %s', tags.AUTO_INVOICING_OFF, account_id)
            return True
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return False

    def create_subscription(self, account_id, product_name, billing_period, price_list):
        payload = self.payloads.get_create_subscription_payload(account_id, product_name, billing_period, price_list)
        response = self.httpClient.do_post('/subscriptions', payload)

        if response.status_code == 201:
            new_object_id = response.headers['Location'][-36:]
            logging.info('Subscription id=%s, product name=%s', new_object_id, product_name)
            return new_object_id
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return None

    def get_invoices_for_account(self, account_id):
        response = self.httpClient.do_get('/accounts/' + account_id + '/invoices?withItems=true')

        if response.status_code == 200:
            logging.debug("\ninvoices:\n%s\n", response.text)
            return json.loads(response.text)
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return None

    def create_invoice_payment(self, account_id, invoice_id, amount, payment_method):
        payload = self.payloads.get_create_invoice_payment_payload(account_id, invoice_id, amount, payment_method)
        response = self.httpClient.do_post('/invoices/' + invoice_id + '/payments?externalPayment=false', payload)

        if response.status_code == 201:
            new_object_id = response.headers['Location'][-37:-1]
            logging.info('Payment id=%s with payment method id=%s for invoice id=%s has been created', new_object_id, payment_method, invoice_id)
            return new_object_id
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return None

    def get_invoice_payment(self, invoice_payment_id):
        response = self.httpClient.do_get('/invoicePayments/' + invoice_payment_id)

        if response.status_code == 200:
            logging.debug("\npayment:\n%s\n", response.text)
            return json.loads(response.text)
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return None

    def write_off_invoice(self, invoice_id):
        response = self.httpClient.do_post('/invoices/' + invoice_id + '/tags?tagList=' + tags.WRITTEN_OFF, None)
        status_code = response.status_code

        if status_code == 201:
            logging.info('Invoice %s has been tagged with WRITTEN_OFF(%s) ', invoice_id, tags.WRITTEN_OFF)
            return True
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return False

    def cancel_subscription(self, subsciption_id):
        params = 'requestedDate=' + time.strftime("%Y-%m-%dT%H:%M:%S.000%z", time.localtime())
        params = params + '&entitlementPolicy=IMMEDIATE'
        params = params + '&useRequestedDateForBilling=false'
        params = params + '&callCompletion=false'
        params = params + '&callTimeoutSec=-1'
        params = params + '&billingPolicy=IMMEDIATE'

        response = self.httpClient.do_delete('/subscriptions/' + subsciption_id + '?' + params)
        status_code = response.status_code

        if status_code == 200:
            logging.info('Subscription with id=%s has been cancelled', subsciption_id)
            return True
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return False

    def get_tenant(self, api_key):
        response = self.httpClient.do_get('/tenants?apiKey=' + api_key)

        if response.status_code == 200:
            return json.loads(response.text)

        return None

    def create_tenant(self, api_key, api_secret):
        payload = {'apiKey': api_key, 'apiSecret': api_secret}
        response = self.httpClient.do_post('/tenants', json=payload)

        if response.status_code == 201:
            new_object_id = response.headers['Location'][-36:]
            logging.info('Tenant created id=%s, api_key=%s, api_secret=%s', new_object_id, api_key, api_secret)
            return new_object_id
        else:
            logging.error('status code=%s, response text=%s', response.status_code, response.text)

        return None

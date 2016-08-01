import uuid


class KillBillRequestPayloads:

    def get_create_invoice_payment_payload(self, account, invoice, amount, payment_method):
        payload = {
            'accountId': account,
            'targetInvoiceId': invoice,
            'purchasedAmount': amount,
            'paymentMethodId': payment_method,
            'currency': 'USD'
        }

        return payload

    def get_create_subscription_payload(self, account, product_name, billing_period, price_list, phase_type):
        payload = {
            'accountId': account,
            'productName': product_name,
            'productCategory': 'BASE',
            'billingPeriod': billing_period,
            'priceList': price_list,
            'phaseType': phase_type
        }

        return payload

    def get_create_account_payload(self, name, external_key):
        payload = {
            'externalKey': external_key,
            'name': name,
            'currency': 'USD',
            'email': 'rvallejo_' + str(uuid.uuid1()) + '@rocketlawyer.com'
        }

        return payload

    def get_create_payment_method_payload(self, account, plugin, number, cvv, month, year):
        payload = {
            'accountId': account,
            'pluginName': plugin,
            'pluginInfo': {
                'properties': [
                    {
                        'key': 'ccFirstName',
                        'value': 'first_name',
                        'isUpdatable': 'false'
                    },
                    {
                        'key': 'ccLastName',
                        'value': 'last_name',
                        'isUpdatable': 'false'
                    },
                    {
                        'key': 'ccNumber',
                        'value': number,
                        'isUpdatable': 'false'
                    },
                    {
                        'key': 'ccVerificationValue',
                        'value': cvv,
                        'isUpdatable': 'false'
                    },
                    {
                        'key': 'ccExpirationMonth',
                        'value': month,
                        'isUpdatable': 'false'
                    },
                    {
                        'key': 'ccExpirationYear',
                        'value': year,
                        'isUpdatable': 'false'
                    },
                    {
                        'key': 'ccZip',
                        'value': '94103',
                        'isUpdatable': 'false'
                    },
                    {
                        'key': 'ccType',
                        'value': 'VISA',
                        'isUpdatable': 'false'
                    }
                ]
            }
        }

        return payload

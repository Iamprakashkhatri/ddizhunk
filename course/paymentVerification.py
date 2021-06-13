def EsewaPaymentVerification(refId, amount,pk):
    import xml.etree.ElementTree as ET
    url ="https://uat.esewa.com.np/epay/transrec"
    d = {
    'amt': amount,
    'scd': 'epay_payment',
    'rid': refId,
    'pid':pk,
    }
    resp = requests.post(url, d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    print('status',status)
    if status =="Success":
        return True
    else:
        return False


def KhaltiPaymentVerification(token, amount):
    payload = {
        "token": token,
        "amount": amount,
    }
    headers = {
        "Authorization": "Key {}".format(settings.KHALTI_SECRET_KEY)
    }
    try:
        response = requests.post(settings.KHALTI_VERIFY_URL, payload,
                                 headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.HTTPError as e:
        return False
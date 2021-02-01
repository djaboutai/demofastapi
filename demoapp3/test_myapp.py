from fastapi.testclient import TestClient

from .myapp import app

import pytest

test_client = TestClient(app)


# Test /payment_process method [POST] with creditcardnumber and status_code [(1111111111111111, 200), (333333333333333, 422)])
@pytest.mark.parametrize("creditcardnumber, status_code, response_code", [(1111111111111111, 200, {
    "creditcardnumber": "1111111111111111",
    "cardholder": "SamirOmar",
    "expirationdate": "2021-02-15",
    "securitycode": "111",
    "amount": 1.0,
    "message_date": True,
    "message_external_api": {
        "status": "200",
        "msg": "Cheap Payment achieved",
        "times": 1
    }
}), (333333333333333, 422, {
    "detail": [
        {
            "loc": [
                "query",
                "creditcardnumber"
            ],
            "msg": "ensure this value has at least 16 characters",
            "type": "value_error.any_str.min_length",
            "ctx": {
                "limit_value": 16
            }
        }
    ]
})])
def test_post_payment_process_creditcardnumber(creditcardnumber, status_code, response_code):
    url_test = f"/paymentprocess?creditcardnumber={str(creditcardnumber)}&cardholder=SamirOmar&securitycode=111&amount=1&expirationdate=2021-02-15"
    response = test_client.post(url=url_test,
                                headers={"Content-Type": "application/json"})

    assert response.status_code == int(status_code)
    assert response.json() == response_code


# Test /payment_process method [POST] with amount [1.0, 10.0, 20.0]
@pytest.mark.parametrize("amount", [1.25, 10.0, 20.98])
def test_post_payment_process_amount(amount):
    url_test = f"/paymentprocess?creditcardnumber=1111111111111111&cardholder=SamirOmar&securitycode=111&amount={str(amount)}&expirationdate=2021-02-15"
    response = test_client.post(url=url_test,
                                headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert response.json() == {
        "creditcardnumber": "1111111111111111",
        "cardholder": "SamirOmar",
        "expirationdate": "2021-02-15",
        "securitycode": "111",
        "amount": amount,
        "message_date": True,
        "message_external_api": {
            "status": "200",
            "msg": "Cheap Payment achieved",
            "times": 1
        }
    }

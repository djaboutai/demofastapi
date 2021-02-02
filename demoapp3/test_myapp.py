import pytest
from fastapi.testclient import TestClient

from .myapp import app
from .payment.process_controller import ControlDatetime, RequestExternalApiControllingAmount


test_client = TestClient(app)


# Test /payment_process method [POST] with creditcardnumber and status_code [(1111111111111111, 200),
# (333333333333333, 422)])
@pytest.mark.parametrize("creditcardnumber, status_code, response_msg", [(1111111111111111, 200, {
    "creditcardnumber": "1111111111111111",
    "cardholder": "JohnDoe",
    "expirationdate": "2021-02-15",
    "securitycode": "111",
    "amount": 1.0,
    "message_date": True,
    "message_external_api": {
        "status": 200,
        "gateway": "cheap",
        "msg": "payment achieved",
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
def test_get_payment_process_creditcardnumber(creditcardnumber, status_code, response_msg):
    url_test = f'/paymentprocess?creditcardnumber={str(creditcardnumber)}' \
               f'&cardholder=JohnDoe&securitycode=111&amount=1&expirationdate=2021-02-15'
    response = test_client.get(url=url_test,
                               headers={"Content-Type": "application/json"})

    assert response.status_code == status_code
    assert response.json() == response_msg


# Test /payment_process method [POST] with amount [10.0, 19.5]
@pytest.mark.parametrize("amount, status_code, response_msg", [(10.0, 200, {
    "creditcardnumber": "1111111111111111",
    "cardholder": "JohnDoe",
    "expirationdate": "2021-02-15",
    "securitycode": "111",
    "amount": 10.0,
    "message_date": True,
    "message_external_api": {
        "status": 200,
        "gateway": "cheap",
        "msg": "payment achieved",
        "times": 1
    }
}), (19.5, 200, {
    "creditcardnumber": "1111111111111111",
    "cardholder": "JohnDoe",
    "expirationdate": "2021-02-15",
    "securitycode": "111",
    "amount": 19.5,
    "message_date": True,
    "message_external_api": {
        "status": 200,
        "gateway": "cheap",
        "msg": "payment achieved",
        "times": 1
    }
})])
def test_get_payment_process_amount(amount, status_code, response_msg):
    url_test = f'/paymentprocess?creditcardnumber=1111111111111111&cardholder=JohnDoe&' \
               f'securitycode=111&amount={str(amount)}&expirationdate=2021-02-15'
    response = test_client.get(url=url_test,
                               headers={"Content-Type": "application/json"})
    assert response.status_code == status_code
    assert response.json() == response_msg


# Test ControlDatetime class class for SOLID TEST
@pytest.mark.parametrize("server_date, expiration_date, ret_bool",
                         [("2021-02-1", "2021-02-15", True), ("2021-02-16", "2021-02-15", False)])
def test_control_datetime(server_date, expiration_date, ret_bool):
    ctrl_date = ControlDatetime()
    assert ctrl_date(server_date, expiration_date) == ret_bool


# Test RequestExternalApiControllingAmount class for SOLID TEST
@pytest.mark.parametrize("creditcardnumber, cardholder, securitycode, amount, expirationdate, ret",
                         [("1111111111111111", "JohnDoe", "111", 15.0, "2021-02-15", 200)])
def test_request_external_api_control_amount(creditcardnumber, cardholder, securitycode, amount, expirationdate, ret):
    ctrl_amount_external_api_result = RequestExternalApiControllingAmount()
    ret_external_api = ctrl_amount_external_api_result(creditcardnumber, cardholder,
                                                       securitycode, amount, expirationdate)
    assert ret_external_api['status'] == ret

import requests
from datetime import datetime


class RequestExternalAPI:
    """
    The RequestExternalAPI is the main class that requests to external payment gateway.
    All changes need to be done here.
    """

    @classmethod
    def payment_gateway_model_out(cls, gate: str = "N/A", msg: str = "Internal Server Error.", status_code: int = 500,
                                  times: int = 0):
        """
        External API return message model.
        :param gate: The used gateway to request payment.
        :param status_code: The status code of the request. If not provided, 500 [INTERNAL ERROR] is used.
        :param msg: The message of the request.
        :param times: The number of times repeated by the gateway.
        :return: Return dict of external api status code, message, gateway and number of times tried.
        """
        return {"status": status_code, "gateway": gate, "msg": msg, "times": times}

    @classmethod
    def request(cls, dump, gateway="N/A", url="www.api.payment/gateway/",
                params="creditcardnumber=1111111111111111&cardholder=JohnDoe"
                       "&securitycode=111&amount=19.2&expirationdate=2021-01-31"):
        """
        This function is the base of external API request. ca
        :param dump: The dummy data returned as not available test or dummy EXTERNAL API GATEWAY.
        :param gateway: The chosen gateway account of amount.
        :param url: The main URL of the EXTERNAL API GATEWAY.
        :param params: The parameters given as query to facilitate the requests.
        :return: Return dict of external api status code, message, gateway and number of times tried.
        """
        if dump:
            return cls.payment_gateway_model_out(gateway, f"payment achieved", 200)
        else:
            r = requests.get(f'{url}{gateway}/{params}')
            print(f'Return  {r}')
            return cls.payment_gateway_model_out(gateway, f"payment achieved", r.status_code)


class RequestInterface(RequestExternalAPI):
    """
    RequestExternalAPI is a static class that separate external payment gateway request and payment process controllers.
    """

    def __init__(self):
        super(RequestExternalAPI, self)

    @classmethod
    def request_cheap(cls, dump, url="www.api.cheap/payment/gateway",
                      params="creditcardnumber=1111111111111111&cardholder=JohnDoe"
                             "&securitycode=111&amount=19.2&expirationdate=2021-01-31"):
        """
        Example of request external API for CHEAP.
        :param dump: True for dummy response.
        :param url: The external URL for cheap gateway.
        :param params: Default full query.
        :return: Return dict of external api status code, message, gateway and number of times tried.
        """
        return cls.request(dump=dump, gateway="cheap", url=url, params=params)

    @classmethod
    def request_expensive(cls, dump, url="www.api.expensive/payment/gateway",
                          params="creditcardnumber=1111111111111111&cardholder=JohnDoe"
                                 "&securitycode=111&amount=19.2&expirationdate=2021-01-31"):
        """
        Example of request external API for EXPENSIVE.
        :param dump: True for dummy response.
        :param url: The external URL for expensive gateway.
        :param params: Default full query.
        :return: Return dict of external api status code, message, gateway and number of times tried.
        """
        return cls.request(dump=dump, gateway="expensive", url=url, params=params)

    @classmethod
    def request_premium(cls, dump, url="www.api.premium/payment/gateway",
                        params="creditcardnumber=1111111111111111&cardholder=JohnDoe"
                               "&securitycode=111&amount=19.2&expirationdate=2021-01-31"):
        """
        Example of request external API for PREMIUM.
        :param dump: True for dummy response.
        :param url: The external URL for premium gateway.
        :param params: Default full query.
        :return: Return dict of external api status code, message, gateway and number of times tried.
        """
        return cls.request(dump=dump, gateway="premium", url=url, params=params)


class RequestExternalApiControllingAmount:
    """
    RequestExternalApiControllingAmount is the controller amount that use only RequestExternalAPI.
    """

    def __init__(self):
        self.request_interface = RequestInterface()

    def __call__(self, creditcardnumber, cardholder, securitycode, amount, expirationdate, params: str = ""):
        """
        :param creditcardnumber: The credit card number in string.
        :param cardholder: The card holder in string.
        :param securitycode: The security code number in string.
        :param amount: The amount of purchase in float.
        :param expirationdate: The expiration date in string.
        :param params: All parameters in string in case of query use.
        :return: Return RequestExternalAPI.payment_gateway_model_out message output model as dict.
        """
        # Call CHEAP here else return 404
        if amount <= 20:
            times: int = 0

            ret = self.request_interface.request_cheap(True)
            if ret['status'] == 200:
                times += 1
                ret['times'] = times
                return ret
            elif ret['status'] == 404:
                times += 1
                ret['times'] = times
                return self.request_interface.payment_gateway_model_out("Cheap", f"No Payment", 404, times)
            else:
                times += 1
                ret['times'] = times
                return self.request_interface.payment_gateway_model_out("Cheap", f"Payment Bad Request", 400, times)

        # TODO: What about 20 < amount <= 21 ???
        # Call EXPENSIVE, if not respond cal ONCE Cheap else CHEAP 404
        elif 21 < amount < 500:
            times: int = 0

            ret = self.request_interface.request_expensive(True)
            if ret['status'] == 200:
                times += 1
                ret['times'] = times
                return ret
            elif ret['status'] == 404 or 400:
                times += 1
                ret['times'] = times
                ret_once = self.request_interface.request_cheap(True)
                if ret_once['status'] == 200:
                    times += 1
                    ret_once['times'] = times
                    return ret_once
                else:
                    times += 1
                    return self.request_interface.payment_gateway_model_out("Cheap", f"No Payment", 404, times)
            else:
                times += 1
                ret['times'] = times
                return ret

        # Call PREMIUM , if not respond try 3TIMES AGAIN PREMIUM else return 404
        elif amount >= 500:
            times: int = 0

            for i in range(3):
                ret = self.request_interface.request_premium(True)
                if ret['status'] == 200:
                    times += 1
                    ret['times'] = times
                    return ret
                elif ret['status'] == 404 or 400:
                    times += 1
                    ret['times'] = times
                    if times == 3:
                        return self.request_interface.payment_gateway_model_out("Premium", f"No Payment", ret['status'],
                                                                                times)
                    continue
                else:
                    times += 1
                    ret['times'] = times
                    if times == 3:
                        return self.request_interface.payment_gateway_model_out("Premium No Payment", ret['status'],
                                                                                times)
                    continue
        else:
            return self.request_interface.payment_gateway_model_out()


class ControlDatetime:
    """
    ControlDatetime class control if the expiration date provided is in the past.
    """

    def __call__(self, server_date, expiration_date):
        """
        :param server_date: The server date of the request.
        :param expiration_date: The credit card expiration date provided.
        :return: bool: True if expiration_date is in future, False if it is in past.
        """
        delta = (datetime.strptime(expiration_date, '%Y-%m-%d')) - (datetime.strptime(server_date, '%Y-%m-%d'))
        return True if delta.days >= 0 else False

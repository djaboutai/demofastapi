from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests


class RequestExternalAPI:
    @classmethod
    def payment_gateway_model_out(cls, s_code, msg, times=0):
        return {"status": str(s_code), "msg": str(msg), "times": times}

    @classmethod
    def request_cheap(cls, dump, url="www.api.cheappaymentgateway",
                      params="creditcardnumber=1111111111111111&cardholder=SamirOmar"
                             "&securitycode=111&amount=19.2&expirationdate=2021-01-31"):
        """Example of request external API for CHEAP"""
        if dump:
            return cls.payment_gateway_model_out(200, "Cheap Payment achieved")
        else:
            r = requests.get(f'{url}{params}')
            print(f'Return  {r}')
            return cls.payment_gateway_model_out(int(r.status_code), "Cheap Payment achieved")

    @classmethod
    def request_expensive(cls, dump, url="www.api.expensivepaymentgateway",
                          params="creditcardnumber=1111111111111111&cardholder=SamirOmar"
                                 "&securitycode=111&amount=19.2&expirationdate=2021-01-31"):
        """Example of request external API for EXPENSIVE"""
        if dump:
            return cls.payment_gateway_model_out(200, "Expensive Payment achieved")
        else:
            r = requests.get(f'{url}{params}')
            print(f'Return  {r}')
            return cls.payment_gateway_model_out(int(r.status_code), "Expensive Payment achieved")

    @classmethod
    def request_premium(cls, dump, url="www.api.premiumpaymentgateway",
                        params="creditcardnumber=1111111111111111&cardholder=SamirOmar"
                               "&securitycode=111&amount=19.2&expirationdate=2021-01-31"):
        """Example of request external API for PREMIUM"""
        if dump:
            return cls.payment_gateway_model_out(200, "Premium Payment achieved")
        else:
            r = requests.get(f'{url}{params}')
            print(f'Return  {r}')
            return cls.payment_gateway_model_out(int(r.status_code), "Premium Payment achieved")


class RequestExternalApiControllingAmount:
    def __init__(self):
        self.request_external_api = RequestExternalAPI()

    def __call__(self, creditcardnumber, cardholder, securitycode, amount, expirationdate, params):
        # Call CHEAP here else return 404
        if int(amount) <= 20:
            times: int = 0

            ret = self.request_external_api.request_cheap(True)
            if int(ret['status']) == 200:
                times += 1
                ret['times'] = times
                return ret
            elif int(ret['status']) == 404:
                times += 1
                ret['times'] = times
                return self.request_external_api.payment_gateway_model_out(404, "Cheap No Payment", times)
            else:
                times += 1
                ret['times'] = times
                return self.request_external_api.payment_gateway_model_out(400, "Cheap Payment Bad Request", times)

        # TODO: What about 20 < amount <= 21 ???
        # Call EXPENSIVE, if not respond cal ONCE Cheap else CHEAP 404
        elif 21 < int(amount) < 500:
            times: int = 0

            ret = self.request_external_api.request_expensive(True)
            if int(ret['status']) == 200:
                times += 1
                ret['times'] = times
                return ret
            elif int(ret['status']) == 404 or 400:
                times += 1
                ret['times'] = times
                ret_once = self.request_external_api.request_cheap(True)
                if int(ret_once['status']) == 200:
                    times += 1
                    ret_once['times'] = times
                    return ret_once
                else:
                    times += 1
                    return self.request_external_api.payment_gateway_model_out(404, "Cheap No Payment", times)
            else:
                times += 1
                ret['times'] = times
                return ret

        # Call PREMIUM , if not respond try 3TIMES AGAIN PREMIUM else return 404
        elif int(amount) >= 500:
            times: int = 0

            for i in range(3):
                ret = self.request_external_api.request_premium(True)
                if int(ret['status']) == 200:
                    times += 1
                    ret['times'] = times
                    return ret
                elif int(ret['status']) == 404 or 400:
                    times += 1
                    ret['times'] = times
                    if times == 3:
                        return self.request_external_api.payment_gateway_model_out(ret['status'], "Premium No Payment", times)
                    continue
                else:
                    times += 1
                    ret['times'] = times
                    if times == 3:
                        return self.request_external_api.payment_gateway_model_out(ret['status'], "Premium No Payment", times)
                    continue


class ControlDatetime:
    def __call__(self, server_date, expiration_date):
        delta = (datetime.strptime(expiration_date, '%Y-%m-%d')) - (datetime.strptime(server_date, '%Y-%m-%d'))
        return True if delta.days >= 0 else False

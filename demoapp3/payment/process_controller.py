from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests


class ControlAmount:
    def __init__(self):
        pass

    @classmethod
    def payment_gateway_model_out(cls, s_code, msg):
        return {"status": str(s_code), "msg": str(msg), "times": 0}

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

    def __call__(self, creditcardnumber, cardholder, securitycode, amount, expirationdate, params):
        # Call CHEAP here else return 404
        if int(amount) <= 20:
            times: int = 0

            ret = self.request_cheap(True)
            if int(ret['status']) == 200:
                times += 1
                ret['times'] = times
                return ret
            elif int(ret['status']) == 404:
                times += 1
                ret['times'] = times
                return {"status": str(404), "msg": "Cheap Payment No Payment", "times": times}
            else:
                times += 1
                ret['times'] = times
                return {"status": str(400), "msg": "Cheap Payment Bad Request", "times": times}

        # Call EXPENSIVE, if not respond cal ONCE Cheap else CHEAP 404
        elif 21 < int(amount) < 500:
            times: int = 0

            ret = self.request_expensive(True)
            if int(ret['status']) == 200:
                times += 1
                ret['times'] = times
                return ret
            elif int(ret['status']) == 404 or 400:
                times += 1
                ret['times'] = times
                ret_once = self.request_cheap(True)
                if int(ret_once['status']) == 200:
                    times += 1
                    ret['times'] = times
                    return ret
                else:
                    times += 1
                    ret['times'] = times
                    return {"status": str(404), "msg": "Cheap Payment No Payment", "times": times}
            else:
                times += 1
                ret['times'] = times
                return {"status": str(400), "msg": "Cheap Payment Bad Request", "times": times}

        # Call PREMIUM , if not respond try 3TIMES AGAIN PREMIUM else return 404
        elif int(amount) > 500:
            times: int = 0

            # TODO: Return payment_gateway_model_out with min 1 max 3 times of the PREMIUM Gateway
            ret = self.request_premium(True)
            if int(ret['status']) == 200:
                times += 1
                ret['times'] = times
                return ret
            elif int(ret['status']) == 404:
                times += 1
                ret['times'] = times
                return {"status": str(404), "msg": "Cheap Payment No Payment", "times": times}
            else:
                times += 1
                ret['times'] = times
                return {"status": str(400), "msg": "Cheap Payment Bad Request", "times": times}


class ControlDatetime:
    def __call__(self, *args):
        # print(f'Date controller current = {args[0]} {type(args[0])} expiration = {args[1]} {type(args[1])}')
        server_date_obj = datetime.strptime(args[0], '%Y-%m-%d')
        request_date_obj = datetime.strptime(args[1], '%Y-%m-%d')
        delta = request_date_obj - server_date_obj
        # print(f'Date controller return {True if delta.days >= 0 else False}')
        return True if delta.days >= 0 else False

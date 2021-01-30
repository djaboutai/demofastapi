from datetime import datetime


class ControlAmount:
    # def __init__(self, amount):
    #     self.amount = amount

    def __call__(self, *args):
        if args[0] <= 20:
            # Call CHEAP here else return 404
            return "CHEAP activated"
        elif 21 < args[0] < 500:
            # Call EXPENSIVE, if not respond cal ONCE Cheap else CHEAP 404
            return "EXPENSIVE activated"
        elif args[0] > 500:
            # Call PREMIUM , if not respond try 3TIMES AGAIN PREMIUM else return 404
            return "PREMIUM activated"


class ControlDatetime:
    @classmethod
    def split_dates(cls, server_date, request_date, sep=" "):
        return set(server_date.split(sep)), set(request_date.split(sep))

    # def split_dates_by_space(cls, server_date, request_date, sep):
    #     return set(server_date.split(sep)), set(request_date.split(sep))
    #
    # def split_dates_by_space(cls, server_date, request_date, sep):
    #     return set(server_date.split(sep)), set(request_date.split(sep))

    def __call__(self, *args):
        # TODO: the format do not perform well.
        print(f'server_date_obj {args[0]} request_date_obj {args[1]}')
        server_date_obj = datetime.strptime(args[0], '%y-%m-%d')
        request_date_obj = datetime.strptime(args[1], '%y-%m-%d')
        print(f'server_date_obj {server_date_obj} request_date_obj{request_date_obj}')
        return

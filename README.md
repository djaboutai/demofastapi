# demofastapi
__This repository shows 2 examples of FastAPI module.__ <br>

## demoapp1
This first repository is a basic example which contains only:
* `route` [GET]  `"/"` <br>
* `route` [GET]  `"/home"` <br>

## demoapp2
This second repository is a more complex which contains:
* `route` [GET]  `"/"` <br>
* `route` [GET]  `"/items/"` <br>
* `route` [GET]  `"/items/{item_id}"` <br>
* `route` [PUT]  `"/items/{item_id}"` <br>
* `route` [GET]  `"/users/"` <br>
* `route` [GET]  `"/users/me"` <br>
* `route` [GET]  `"/users/{username}"` <br>
* `route` [POST] `"/admin/"` <br>
* `route` [GET]  `"/admin/redirect"` <br>
* `route` [POST] `"/admin/login"` <br>

__demoapp2__ also has implemented:
* `FastAPI app with -title -description -dependencies -openapi_tags -version`
* `Static files mount`
* `Middleware CORS included`
* `Include router from myapp.py with -prefic -tags -responses`
* `Controllers called by modules with -summary`

## demoapp3
This third repository is a demo of a process payment by Card using only 1 method:
* `route`   [POST]  `"/paymentprocess"` with queries:
    * creditcardnumber `string` <br>
    * cardholder `string` <br>
    * securitycode `string` <br>
    * amount `float` <br>
    * expirationdate `string` <br>

You can also see it at `/docs` after running the demo with `uvicorn demoapp3.myapp:app --reload --port xxxx`. <br>
You can also perform test with `pytest demoapp3` with integrated 5 test cases.

## how to run
Simple as hello, you just need to:
* First install requirements by `pip install -r requirements.txt` <br>
* And run `uvicorn demoapp1.myapp:app --reload --port xxxx` <br>
* Want to see api description? go to `localhost/docs` <br>
* Want to test api? run `pytest demoappX` <br>
* ... and then, it is done. <br>
* __YOU ARE FREE TO RUN WHATEVER YOU WANT__ :innocent:

## authors
* Samir Omar {main contributor} :blush:

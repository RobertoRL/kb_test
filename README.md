# kb_test

## Requirements
- Python 2.7.10
- Requests: `pip install requests`

## Running the test
1) Download killbill jetty console
```
$ wget https://repo1.maven.org/maven2/org/kill-bill/billing/killbill-profiles-killbill/0.16.7/killbill-profiles-killbill-0.16.7-jetty-console.war
```

2) Start killbill (use defaults)
```
$ java -jar killbill-profiles-killbill-0.16.7-jetty-console.war
```

3) Create tenant
```
$ curl -v \
     -X POST \
     -u admin:password \
     -H 'Content-Type: application/json' \
     -H 'X-Killbill-CreatedBy: admin' \
     -d '{"apiKey": "bob", "apiSecret": "lazar"}' \
     "http://127.0.0.1:8080/1.0/kb/tenants"
```

4) Run test
```
$ python main.py
```

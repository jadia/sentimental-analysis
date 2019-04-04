# sentimental-analysis
Analyse sentiments of people about 2019 election via twitter.

APIs are supported along with Web interface.

## How to use API

```bash
curl http://localhost:5000/api/Rahul,Congress,Amethi
```

if spaces are there between the requests then use services like POSTMAN which automatically replaces spaces with `%20`

```bash
curl http://localhost:5000/api/Modi,Amit Shah,BJP
```

**NOTE:** twitterCredentials.py file is not included in the repo to prevent exposure of user's twitter API.

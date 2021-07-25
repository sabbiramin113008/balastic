# Balastic

A Toy Application for Playing with Elastic Search APIs.

## Environment Preparation

---

1. Installing and running `elasticsearch server` is beyond this documentation scope. Please follow, [`https://www.elastic.co/`](https://www.elastic.co/) for head start and all the tutorials.
2. Make sure `venv` or any virtual environment is installed. If not, try, `sudo apt-get install python3-venv` and also, please make sure the pip is upgraded to the latest version. If Not, then try `pip install ---upgrade pip`
3. If you are using `venv` make sure to activate it via `source venv/bin/activate`.
4. Make sure to install the exact same version of the modules docked in `requirements.txt`. Type `pip install -r requirements.txt` on terminal and you are ready to go.

### Work Flow and Summary of the Solution Approach

---

1. Please run `python populate_data.py` script for the initial `curl` data file creation followed by `json` file generation. 
2. As tweaking the elastic search over HTTP API is super easy, to answer all the questions, all the `curl` commands are added in the `[readme.md](http://readme.md)` file as well as respective `Insomnia_API_collection` can be found in `insomnia_docs` directory. 
3. For load testing `locust` a load testing framework is added. All the necessary files can be found in `locustfiles` dir. To run the test, please run `locust -f locustfiles/ElasticServerTest.py` to start the test server. This will start an web interface at [http://0.0.0.0:8089](http://0.0.0.0:8089/) (accepting connections from all network interfaces). 

### 1. Creating the Index

---

```bash
curl --request PUT \
  --url http://localhost:9200/paper-index \
  --header 'Content-Type: application/json'
```

### 2. Bulk Insert from the File

---

```bash
λ curl -i -X POST \
 --url localhost:9200/_bulk \
 --header "Content-Type: application/x-ndjson" \
 --data-binary "@bulk_insertion_paper_data.txt"
```

The contents of the `bulk_insertion_paper_data.txt` are as follows, 

```
{"index" : {"_index" : "paper_index", "_id":"1" }\n
{"reseachId":1,"author":"Sarah Morse", "publishDate":"2017-10-15", "status":"REJECTED", "researchText":"Memory nor interesting which talk tree part. Life seek before describe always morning into.Camera dark spring with life onto. Note health scientist ask.Process budget many picture." }
{"index" : {"_index" : "paper_index", "_id":"2" }\n
{"reseachId":2,"author":"Antonio Henderson", "publishDate":"2008-07-03", "status":"REJECTED", "researchText":"One discover government. Stop remain quite finish.Security evidence floor condition true. Half behavior measure camera. Picture simply parent two." }
{"index" : {"_index" : "paper_index", "_id":"3" }\n
{"reseachId":3,"author":"Aaron Rivera", "publishDate":"2017-08-17", "status":"REJECTED", "researchText":"Career network various rate maybe. Nature drug least even.Wonder try name. Present source from security." }
{"index" : {"_index" : "paper_index", "_id":"4" }\n
{"reseachId":4,"author":"Matthew Phillips DDS", "publishDate":"2013-02-14", "status":"ACCEPTED", "researchText":"Election view help arrive series. Risk agency recognize never line seven everyone actually. Learn cut gun appear person party hope. One fight role effect whose." }
{"index" : {"_index" : "paper_index", "_id":"5" }\n
{"reseachId":5,"author":"David Willis", "publishDate":"2006-11-23", "status":"SUBMITTED", "researchText":"These price behind environment. Trip dog Mrs brother people also sing particular. Skin full myself art require head.Me although enjoy nation new fund. Foreign agent one loss. Doctor party bar." }
{"index" : {"_index" : "paper_index", "_id":"6" }\n
{"reseachId":6,"author":"Spencer Mcgrath", "publishDate":"2021-06-29", "status":"SUBMITTED", "researchText":"Step pattern case among. Everyone card woman save. Evening sure military still foreign hold.Voice investment whose rock baby. Determine pay last effect." }
.....
```

### 3. Updating Data by Doc Ids

---

Let's assume papers with  `Ids=[4, 5, 6]` are `REJECTED` in the examining process and their status should be changed to `REJECTED` . Now we are going to update these docs using `painless`

The logic is we will check if the current status is equal to `SUBMITTED` only then it will change the status to `REJECTED` . 

**Single Instance Command**

```bash
curl --request POST \
  --url http://localhost:9200/paper_index/_update/5 \
  --header 'Content-Type: application/json' \
  --data '{
	"script":{
		"lang":"painless",
		"source":"if (ctx._source.status.contains('\''SUBMITTED'\'')){ctx._source.status = '\''REJECTED'\''}"
	}
}'
```

**Bulk Update Using Bulk API and `painless`** 

```bash
curl --request POST \
  --url http://localhost:9200/_bulk \
  --header 'Content-Type: application/x-ndjson' \
  --data '{"update":{"_id":"4", "_index":"paper_index"}}
{"script": {"source": "if (ctx._source.status.contains('\''SUBMITTED'\'')){ctx._source.status='\''REJECTED'\''}","lang": "painless"}}
{"update":{"_id":"5", "_index":"paper_index"}}
{"script": {"source": "if (ctx._source.status.contains('\''SUBMITTED'\'')){ctx._source.status='\''REJECTED'\''}","lang": "painless"}}
{"update":{"_id":"6", "_index":"paper_index"}}
{"script": {"source": "if (ctx._source.status.contains('\''SUBMITTED'\'')){ctx._source.status='\''REJECTED'\''}","lang": "painless"}}

'
```

### 4. Changing `status` from `STRING` to `Int` Value

We will use `painless` script to change `status` field of all the docs with the following command. 

```bash
curl --request POST \
  --url http://localhost:9200/paper_index/_update_by_query \
  --header 'Content-Type: application/json' \
  --data '{
  "script": {
    "source": "if (ctx._source.status.equals('\''SUBMITTED'\'')){ctx._source.status=0} if (ctx._source.status.equals('\''ACCEPTED'\'')){ctx._source.status=1}if (ctx._source.status.equals('\''REJECTED'\'')){ctx._source.status=2}",
    "lang": "painless"
  }
}'
```

### 5. Adding `category` field to Each of the Document.

```bash
curl --request POST \
  --url http://localhost:9200/paper_index/_update_by_query \
  --header 'Content-Type: application/json' \
  --data '{
  "script": {
    "source": "if (ctx._source.status.equals(0)){ctx._source.category='\''submitted'\''} if (ctx._source.status.equals(1)){ctx._source.category='\''accepted'\''}if (ctx._source.status.equals(2)){ctx._source.category='\''rejected'\''}",
    "lang": "painless"
  }
}'
```
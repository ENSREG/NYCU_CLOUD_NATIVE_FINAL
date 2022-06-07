# NYCU Cloud Native Final Project

![image](https://user-images.githubusercontent.com/42661015/170951173-2a5430a9-2ec2-4b22-a0a2-0d40483f027b.png)

## 專案結構

```
.
.
├── frontend
│   ├── img
│   │   └── graph.ico
│   ├── index.html
│   ├── my_chart.js
│   └── style.css
├── images
│   ├── crawler
│   │   ├── ckpt
│   │   │   └── BayesianRidge.pkl
│   │   ├── data
│   │   │   ├── GroundTruth.csv
│   │   │   └── Pred.csv
│   │   ├── header
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-37.pyc
│   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   ├── evaluate.cpython-37.pyc
│   │   │   │   ├── model.cpython-37.pyc
│   │   │   │   └── utils.cpython-37.pyc
│   │   │   ├── crawler
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__
│   │   │   │   │   ├── __init__.cpython-37.pyc
│   │   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   │   ├── crawler.cpython-37.pyc
│   │   │   │   │   └── crawler.cpython-38.pyc
│   │   │   │   └── crawler.py
│   │   │   └── model
│   │   │       ├── __init__.py
│   │   │       ├── __pycache__
│   │   │       │   ├── __init__.cpython-37.pyc
│   │   │       │   ├── __init__.cpython-38.pyc
│   │   │       │   ├── evaluate.cpython-37.pyc
│   │   │       │   ├── model.cpython-37.pyc
│   │   │       │   ├── utils.cpython-37.pyc
│   │   │       │   └── utils.cpython-38.pyc
│   │   │       ├── evaluate.py
│   │   │       └── utils.py
│   │   ├── main_crawler.py
│   │   ├── main_model.ipynb
│   │   ├── readme.md
│   │   ├── requirements.txt
│   │   ├── run.py
│   │   ├── test_crawler.py
│   │   └── test_model.py
│   └── flask
│       ├── Crawler_env
│       ├── Dockerfile
│       ├── readme.md
│       ├── requirements.txt
│       └── run.py
├── nycu-cloud-final
│   ├── Chart.yaml
│   ├── templates
│   │   ├── NOTES.txt
│   │   ├── _helpers.tpl
│   │   ├── deployment.yaml
│   │   ├── hpa.yaml
│   │   ├── ingress.yaml
│   │   ├── service.yaml
│   │   ├── serviceaccount.yaml
│   │   └── tests
│   │       └── test-connection.yaml
│   └── values.yaml
├── readme.md
└── total.csv
```

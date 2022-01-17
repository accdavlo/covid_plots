PROJECT:=covidplots
BUILD_TAG?=v2.0

run:
	streamlit run app.py --server.port=8080 --server.address=0.0.0.0

run-container:
	docker build -t $(PROJECT):${BUILD_TAG} .
	docker run -d --name $(PROJECT)-${BUILD_TAG}-container -it --rm -p 8080:8080 $(PROJECT):${BUILD_TAG}

del:
	docker stop $(PROJECT)-${BUILD_TAG}-container
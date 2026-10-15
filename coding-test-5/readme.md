Run the Docker image using this command: 

docker build -t receipt-app .
docker run -p 8501:8501 --env-file ..\.env -v "${PWD}\data:/app/data" receipt-app
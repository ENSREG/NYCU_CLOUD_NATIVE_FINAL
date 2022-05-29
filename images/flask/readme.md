# Flask and python environment test

## Network explaination
I just port forward local:80 to container:80 in bridge mode.
If you want to use another port, please edit ./Crawler_env by yourself.

```bash=
chmod +x Crawler_env

# please add -setup flag at first time
./Crawler_env -setup

# after setup, user can just use like the following
./Crawler_env
```

## Push to dockerhub

```
docker build . -t ianchen0119/nycu_final_flask
docker push ianchen0119/nycu_final_flask
```
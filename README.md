## This project is actively in research and developement 🔭

![xkcd](https://imgs.xkcd.com/comics/engineer_syllogism.png)

## About
Binoculars is a trading bot with Binance API. Binoculars 
exposed some strategy algorithms which are utilized for 
both live and back-testing.

## Disclaimer
This repository is for educational purposes only. 
**Use this software at your own risk!**

## Spark Interactive Container
```bash
sudo docker build -t bino_spark -f Dockerfile .
sudo docker run --rm --network host -it bino_spark /bin/bash
```

Going into the spark directory and start spark shell with Scala,
```
cd /opt/spark/bin && spark-shell
``` 

## TODO
- [x] SMA strategy
- [x] Classification on direction
- [x] DuckDB setup
- [ ] Order Book
- [ ] Testing
- [ ] Microservices (Flask)
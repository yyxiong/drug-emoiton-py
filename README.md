# drug-emotion

## dev

    ```shell
    docker run -it -v /Users/yunuo/Selfspace/Pager/drug-emotion/spiders:/drug-emotion:ro xiongyunuo/drug-emotion-py /bin/bash

    scrapy crawl net39
    ```

## build

    ```shell
    docker build --rm -f "Dockerfile" -t xiongyunuo/drug-emotion-py:latest .
    ```

## run

    ```shell
    docker run -it xiongyunuo/drug-emotion-py
    ```

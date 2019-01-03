# drug-emoiton

## 教程参考

    Scrapy 对接 Docker
    https://juejin.im/post/5ad6f6bcf265da237c696daf

## dev

    ```shell
    docker run -it -v /Users/yunuo/Selfspace/Pager/drug-emotion/spiders:/drug-emotion:ro drug-emotion /bin/bash
    ```

## build

    ```shell
    scrapy startproject net39

    docker build --rm -f "Dockerfile" -t drug-emoiton:latest .
    ```

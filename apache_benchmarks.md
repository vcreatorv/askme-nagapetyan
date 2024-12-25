## Отдача статического документа напрямую через nginx:

```shell
ab -n 1000 -c 10 http://127.0.0.1/static/sample.html
```

```txt
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)


Server Software:        nginx/1.18.0
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /static/sample.html
Document Length:        365 bytes

Concurrency Level:      10
Time taken for tests:   0.336 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      715000 bytes
HTML transferred:       365000 bytes
Requests per second:    2977.38 [#/sec] (mean)
Time per request:       3.359 [ms] (mean)
Time per request:       0.336 [ms] (mean, across all concurrent requests)
Transfer rate:          2078.93 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.0      1       9
Processing:     0    2   1.1      2      10
Waiting:        0    1   1.0      1       9
Total:          1    3   1.5      3      12

Percentage of the requests served within a certain time (ms)
  50%      3
  66%      3
  75%      4
  80%      4
  90%      5
  95%      6
  98%      8
  99%     10
 100%     12 (longest request)
```

## Отдача статического документа напрямую через gunicorn:

```shell
ab -n 1000 -c 10 http://127.0.0.1:8000/static/sample.html
```

```txt
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)


Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /static/sample.html
Document Length:        365 bytes

Concurrency Level:      10
Time taken for tests:   1.675 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      730000 bytes
HTML transferred:       365000 bytes
Requests per second:    597.00 [#/sec] (mean)
Time per request:       16.750 [ms] (mean)
Time per request:       1.675 [ms] (mean, across all concurrent requests)
Transfer rate:          425.59 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       2
Processing:     4   16   3.3     16      27
Waiting:        3   16   3.3     16      27
Total:          4   17   3.3     16      27

Percentage of the requests served within a certain time (ms)
  50%     16
  66%     18
  75%     19
  80%     19
  90%     21
  95%     23
  98%     24
  99%     25
 100%     27 (longest request)
```

## Отдача динамического документа напрямую через gunicorn:

```shell
ab -n 1000 -c 10 http://127.0.0.1:8000/hot/
```

```txt
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)


Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /hot/
Document Length:        613540 bytes

Concurrency Level:      10
Time taken for tests:   1944.835 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      613973000 bytes
HTML transferred:       613540000 bytes
Requests per second:    0.51 [#/sec] (mean)
Time per request:       19448.350 [ms] (mean)
Time per request:       1944.835 [ms] (mean, across all concurrent requests)
Transfer rate:          308.30 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.7      0       9
Processing:  5335 19337 3710.0  18763   30260
Waiting:     5334 19332 3710.5  18757   30258
Total:       5338 19337 3710.0  18763   30269

Percentage of the requests served within a certain time (ms)
  50%  18763
  66%  20535
  75%  21776
  80%  22693
  90%  24881
  95%  26125
  98%  27603
  99%  28642
 100%  30269 (longest request)
```

## Отдача динамического документа через проксирование запроса с nginx на gunicorn:

```shell
ab -n 1000 -c 10 http://127.0.0.1/hot/
```

```txt
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        nginx/1.18.0
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /hot/
Document Length:        613540 bytes

Concurrency Level:      10
Time taken for tests:   6.404 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      613872001 bytes
HTML transferred:       613540000 bytes
Requests per second:    156.15 [#/sec] (mean)
Time per request:       64.042 [ms] (mean)
Time per request:       6.404 [ms] (mean, across all concurrent requests)
Transfer rate:          93608.43 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.4      0       5
Processing:     2   13 178.2      7    5641
Waiting:        0    6 178.3      0    5638
Total:          2   13 178.2      7    5642

Percentage of the requests served within a certain time (ms)
  50%      7
  66%      8
  75%      8
  80%      9
  90%     11
  95%     12
  98%     14
  99%     15
 100%   5642 (longest request)
```

## Отдача динамического документа через проксирование запроса с nginx на gunicorn, при кэшировние ответа на nginx (proxy cache):

```shell
ab -n 1000 -c 10 http://127.0.0.1/
```

```txt
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)


Server Software:        nginx/1.18.0
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /
Document Length:        614548 bytes

Concurrency Level:      10
Time taken for tests:   0.772 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      614880000 bytes
HTML transferred:       614548000 bytes
Requests per second:    1295.75 [#/sec] (mean)
Time per request:       7.718 [ms] (mean)
Time per request:       0.772 [ms] (mean, across all concurrent requests)
Transfer rate:          778058.20 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.4      0       4
Processing:     2    7   1.8      7      14
Waiting:        0    0   0.5      0       4
Total:          3    8   1.9      7      15

Percentage of the requests served within a certain time (ms)
  50%      7
  66%      8
  75%      9
  80%      9
  90%     10
  95%     11
  98%     13
  99%     13
 100%     15 (longest request)
```

## Выводы

Насколько быстрее отдается статика по сравнению с WSGI?
- Nginx обрабатывает примерно в 5 раз больше запросов в секунду (**Requests per second**), имеет в 5 раз меньшее среднее время обработки запроса (**Time per request (mean)**) и в 5 раз выше скорость передачи данных (**Transfer rate**).

Во сколько раз ускоряет работу proxy_cache?
- Кэширование на Nginx (**proxy cache**) в среднем ускоряет обработку запросов в 8 раз по сравнению с проксированием без кэширования и на 2530 раз по сравнению прямым обращением к приложению через Gunicorn.
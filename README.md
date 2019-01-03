# [Baekjoon Online Judge](http://www.acmicpc.net/) Submitted Code Download Tool

## 왜 만들었는가?

- 시험기간이다.

## 설명
    
- BOJ에 제출한 코드 중, 맞은 코드를 한번에 다운받는다.

## 결과물

- 문제 별 폴더가 만들어지고, 문제의 번호를 이름으로 파일이 생성됨. (ex. 1000\1000.py)
    
- 한 문제를 같은 언어로 여러번 맞았을 경우 가장 좋은(시간, 공간 복잡도가 작은) 코드를 다운로드함.
    
- 프로그램을 실행한 폴더에 생성함.

## 종속성

- [python3](https://www.python.org/downloads/)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)

#### Ubuntu

```bash
# 패키지 설치
sudo apt install python3-pip

# beautifulsoup4 설치
pip3 install -r requirements.txt
```

## 사용법

```bash
python3 main.py
```
	
### Issue

- 맞은 코드가 여러 페이지에 걸쳐 있을경우 첫 페이지의 코드만 받음

## Update Log

- 2016/9/6 : 가장 '좋은'코드가 아니라 가장 '안좋은'코드를 선택하던 **치명적인** 문제 해결
- 2016/9/7 : 프로그램이 종료되지 않던 문제 해결, 결과화면 정리
- 2019/1/2 : 페이지 URL 변경으로인한 에러 수정 (thanks to @MilkClouds)

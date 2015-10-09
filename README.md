#[BOJ](https://www.acmicpc.net/) Submitted Code Auto Download Tool

##왜 만들었는가?

- 시험기간이다.

##Tool 사용 환경

- Python3
- Beautiful Soup 4

	###Beautiful Soup 4 설치법
	
	- [설치법](https://www.acmicpc.net/blog/view/16)
	- <B>주의</B> : UNIX에서 pip를 이용할 경우 python3용 pip사용 ([설치](http://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3), 실행 : pip3) 

##Tool 설명
    
- BOJ에 제출한 코드 중, 맞은 코드를 한번에 다운받는다.

##Tool 결과물

- 언어 별 폴더가 만들어지고, 문제의 번호를 이름으로 파일이 생성됨. (ex. Python\1000.py)
    
- 한 문제를 같은 언어로 여러번 맞았을 경우 가장 좋은(시간, 공간 복잡도가 작은) 코드를 다운로드함.
    
- 프로그램을 실행한 폴더에 생성함.

##Tool 사용법

	python3 main.py
	
###Issue

- 맞은 코드가 여러 페이지에 걸쳐 있을경우 첫 페이지의 코드만 받음
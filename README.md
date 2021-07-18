# 망고 플레이트 Clone Project Backend

## 프로젝트 소개
- 망고플레이트란, 사용자 데이터 기반의 식당추천 서비스로 주변 맛집 정보 및 추천 맛집 리스트 등, 종합적인 맛집 발견 경험을 제공하는 사이트입니다.
- 우리의 프로젝트는, 망고플레이트의 기능(맛집 리스트, 검색 필터링, 가고싶다, 리뷰, 평점 등)을 선릉 주변의 실제 식당 데이터에 적용한 클론 프로젝트입니다.
- 짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인 및 기능의 기획 부분만 클론했습니다.
- 개발은 초기 세팅부터 전부 직접 구현했으며, 모두 백앤드와 연결하여 실제 사용할 수 있는 서비스 수준으로 개발한 것입니다.
- [백엔드 github 링크](https://github.com/wecode-bootcamp-korea/20-2nd-BeerBnB-backend)
- [프론트엔드 github 링크](https://github.com/wecode-bootcamp-korea/22-1st-mangoPeace-frontend)

### 개발 인원 및 기간
- 개발기간 : 2021/7/5 ~ 2030/7/16
- 개발 인원 : 백엔드 3명, 프론트엔드 3명
- 백엔드 : [이원석(PM)](https://github.com/wonseok2877), [최준영](https://github.com/showmethr23), [이지훈](https://github.com/wlgns410)
- 프론트엔드 : [정빛열음](https://github.com/kylee817), [이의연](https://github.com/euiyeonlee), [이경민](https://github.com/glorious-min)

### 프로젝트 선정이유
- 위코드 커리큘럼에서 배운 기술들을 그대로 적용하고 응용하는 데에 있어 난이도가 적합하다고 판단했습니다.
- 사용자의 선택에 따라 구분되는 필터링이 매력적이라고 생각했습니다.
- 맛집 추천과 SNS 개념의 접목이 매력적이라고 생각했습니다.

<br>

## 적용 기술 및 구현 기능

### 적용 기술

> - Front-End : javascript, React.js framwork, sass, Kakao Map API
> - Back-End : Python, Django web framework, MySQL, Bcrypt, pyjwt
> - Common : POSTMAN, RESTful API


### 구현 기능

#### 회원가입 / 로그인 모달
- 회원가입 시 정규식을 통한 유효성 검사. (소문자, 대문자, 특수문자의 조합)
- 로그인을 이후 토큰 발행, 계정 활성화
- 계정 없을 시 바로 회원가입 모달로 이동할 수 있도록 구현.

#### 메인페이지

- 검색바에서 키워드 검색시 검색 페이지로 이동.
- 맛집 리스트 배너. 클릭 시 리스트 페이지로 이동.
- TOP5 식당 배너. 클릭 시 해당 식당의 상세 페이지로 이동.
- 하단 푸터를 통한 사이트 설명.

#### 검색 페이지

- 키워드(카테고리, 식당 이름) 필터링.
- 리뷰순, 평점순, 가격대에 대한 세부 필터링.
- 페이지네이션.

#### 리스트페이지

- 카테고리에 대한 식당 리스트를 평점순으로 나열.
- 클릭시 상세 페이지로 이동.

#### 상세페이지

- 위도와 경도를 이용한 kakao map API 구현.
- 식당 상세정보, 음식 사진 정보, 가고싶다 여부.
- 식당에 대한 리뷰 평점순으로 나열, 페이지네이션.
- 가고싶다(위시리스트) 생성, 삭제
- 리뷰 생성, 수정, 삭제

#### 네비게이션 바
- 검색바.
- 회원가입, 로그인 버튼.
- 이름, 사진, 가고싶다 목록 등 유저 정보.


<br>

## Reference

- 이 프로젝트는 [망고플레이트](https://www.mangoplate.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
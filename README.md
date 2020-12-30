# SANTOKI_IOT
---
## 개요
아두이노와 라즈베리 파이로 만들어진 간단한 IOT 시스템 입니다<br>
온도와 습도 데이터를 센서를 통해 아두이노가 수집합니다.<br>
블루투스 4.0 으로 아두이노와 라즈베리 파이가 통신합니다.<br>
라즈베리파이가 허브 역할을 하게 됩니다.<br>
실시간 온도 데이터와 디바이스 정보는 Firebase의 real time DB를 사용하였고<br>
시계열 데이터는 InfluxDB를 사용하여 저장하였습니다.<br>
이후 플라스크 서버 API를 통해 InfluxDB의 시계열 데이터를 가져와서 FrontEnd인 Vue에서<br>
뿌려주게 됩니다.

* 플라스크 실행장면
<img src="https://user-images.githubusercontent.com/69225568/103328075-b8c0e380-4a9a-11eb-9d6a-dccaed71a397.PNG" width="600" alt="라즈베리파이 실행장면">

* InfluxDB와 Granafa 연동을 통한 대시보드

<img src="https://user-images.githubusercontent.com/69225568/103328073-b6f72000-4a9a-11eb-97fe-9a2315f2765c.PNG" width="600" alt="그라파나 대시보드">
<img src="https://user-images.githubusercontent.com/69225568/103328074-b8284d00-4a9a-11eb-8473-2b7ccc4459c1.PNG" width="600" alt="그라파나 대시보드2">

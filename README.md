# [TFT 게임 전 서버 Top10 플레이어 매치 데이터 분석]
*   리더: 신충섭
*   정의: Riot API를 활용하여 수집한 TFT 데이터를 분석하고 시각화합니다.
*   목적: 저장한 TFT 매치 데이터로부터 사용자와 운영진 측면의 게임 메타분석, 특성의 연관규칙 등을 분석할 수 있습니다.
*   범위: 주단위로 수집된 16개의 서버의 Top 10 플레이어 최근 20 경기
    * 분석 대상 : 플레이어, 매치, 유닛, 아이템, 특성
    * 서버 정보는 다음과 같습니다.
    * 브라질(BR1), 유럽서부(EUW1), 유럽북동(EUN1), 일본(JP1), 한국(KR), 라틴아메리카북부(LA1), 라틴아메리카남부(LA2), 북미(NA1), 오세아니아(OC1), 필리핀(PH2), 러시아(RU), 싱가포르(SG2), 태국(TH2), 터키(TR1), 대만(TW2), 베트남(VN2)

* PPT : [TFT 게임 전 서버 Top10 플레이어 매치 데이터 분석](https://github.com/tooha289/TeamFightTactics/blob/main/document/%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B6%84%EC%84%9D(%EC%8B%9C%EA%B0%81%ED%99%94)/TFT%20%EA%B2%8C%EC%9E%84%20%EC%A0%84%20%EC%84%9C%EB%B2%84%20Top10%20%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%20%EB%A7%A4%EC%B9%98%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B6%84%EC%84%9D.pptx)

## 주요 구조 및 파일 설명
### document
* 데이터 수집, 데이터 저장, 데이터 분석 각 프로젝트에 대한 정의서 및 산출물 파일이 포함되어 있습니다.

### tft_analysis
* 전체적인 분석 결과에 해당하는 data_analysis파일과 통계 제공용 파일인 stat 파일이 존재합니다.
  
### team_fight_tactics.py
* RiotApiAdaptor : RiotAPI 사용을 위한 어댑터 클래스입니다.
* TftDataHandler : API를 통해 수집한 데이터를 처리하는 클래스입니다.

---
#### 라이엇 지침
'TeamFightTactics 프로젝트는 라이엇 게임즈가 공인한 것이 아니며, 라이엇 게임즈 또는 리그 오브 레전드 제작 또는 관리에 공식적으로 참여하는 당사자들의 의견이나 관점을 반영하지 않습니다.'

'The TeamFightTactics project is not endorsed by Riot Games and does not reflect the opinions or views of Riot Games or those officially involved in the production or management of League of Legends.'

League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.

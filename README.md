# harry_potter-TRPG_bot
해리포터용 TRPG 봇입니다.
TableTop Roll Playing Game bot of Harry-hotter.
---
(한국어)
## 목차
1. 명령어 (슬래시)
2. 데이터베이스
---
## 1. 명령어
### /마법추가
- 전달인자 : /마법추가 (마법이름) (마법설명) (마법분류) (숙련도) (소모마력)
- 자신의 DB에 사용 가능한 마법을 추가합니다.
- 마법이름 : str 형식으로 저장
- 마법설명 : str 형식으로 저장
- 마법분류 : spell_choices 안에 있는 목록에서 선택. str 형식으로 저장
- 숙련도 1~10 중에 숫자 입력. int 형식으로 저장
- 소모마력 : int 형식으로 저장
### /상태창
- 전달인자 : /상태창
- 자신이 등록한 상태창을 조회합니다.
- (만약 없다면 "등록된 캐릭터 정보가 없습니다."를 자신만 보이게 반환합니다.)
- 상태창 목록 : 이름, 성별, 나이, 기숙사, 학년, 사용가능 마법 및 숙련도 레벨(LV)
### /남은마력
- 전달인자 : /남은마력
- 자신의 남은 마력을 조회합니다.
- (만약 없다면 "등록된 캐릭터 정보가 없습니다."를 자신만 보이게 반환합니다.)
### /마력설정
- 전달인자 : /마력설정 (남은마력) (최대마력)
- 자신의 마력 상태를 설정합니다.
- (만약 캐릭터가 없다면 "등록된 캐릭터 정보가 없습니다."를 자신만 보이게 반환합니다.)
### /마력회복
- 전달인자 : /마력회복 (count : 기본값 1)
- 자신의 마력을 회복합니다. (음수값이라면 차감)
- (만약 설정된 마력이 없다면 "현재 마력이 설정되어있지 않습니다."를 자신만 보이게 반환합니다.)
- 반환 : (이전마력 / 최대마력) -> (현재마력 / 최대마력)
### /마법삭제
- 전달인자 : /마법삭제 (마법이름)
- 자신이 보유한 마법 중 하나를 삭제합니다.
- 마법이름은 자신이 보유한 마법 중 상위 25개까지 자동완성을 제공합니다.
- (만약 입력한 마법을 보유 중이 아니라면 "등록된 마법이 없습니다."를 자신만 보이게 반환합니다.)
### /마법조회
- 전달인자 : /마법조회 (마법이름)
- 자신이 보유한 마법 중 하나를 조회합니다.
- 마법이름은 자신이 보유한 마법 중 상위 25개까지 자동완성을 제공합니다.
- (만약 입력한 마법을 보유 중이 아니라면 "등록된 마법이 없습니다."를 자신만 보이게 반환합니다.)
- 반환 : 마법이름, 마법설명, 마법분류, 숙련도, 소모마력
### /마법사용
- 전달인자 : /마법사용 (마법이름)
- 자신이 보유한 마법 중 하나를 사용합니다.
- 마법이름은 자신이 보유한 마법 중 상위 25개까지 자동완성을 제공합니다.
- (만약 입력한 마법을 보유 중이 아니라면 "등록된 마법이 없습니다."를 자신만 보이게 반환합니다.)
- 사용한 마법에 등록된 (소모마력)만큼 자신의 현재마력을 차감합니다.
- (만약 설정된 마력이 없다면 "현재 마력이 설정되어있지 않습니다."를 자신만 보이게 반환합니다.)
- (만약 마력이 부족하다면 "(부족한 MP양)이 부족합니다."를 반환합니다.)
- 반환 : "마법이름" (전체 메시지), "소모 MP, 마법사용 결과" (개인 메시지)
### /소모마력조정
- 전달인자 : /소모마력조정 (마법이름) (소모마력)
- 자신이 보유한 마법 중 하나의 소모마력을 조정합니다.
- 마법이름은 자신이 보유한 마법 중 상위 25개까지 자동완성을 제공합니다.
- (만약 입력한 마법을 보유 중이 아니라면 "등록된 마법이 없습니다."를 자신만 보이게 반환합니다.)
### /마법숙련도조정
- 전달인자 : /마법숙련도조정 (마법이름) (소모마력)
- 자신이 보유한 마법 중 하나의 숙련도를 조정합니다.
- 마법이름은 자신이 보유한 마법 중 상위 25개까지 자동완성을 제공합니다.
- (만약 입력한 마법을 보유 중이 아니라면 "등록된 마법이 없습니다."를 자신만 보이게 반환합니다.)
---
## 데이터베이스
    magic_point
    | user's discord id | points | max_points |

    status
    | user's discord id | character_name | sex | age | dormitory | grade |

    user_spells
    | user's discord id | spells(json) |
---
(English)
## Table of Contents
1. Command (slash)
2. Database
---
## 1. Command
### /Add Magic
- Arguments : /Add Magic (Magic Name) (Magic Description) (Magic Category) (Skill Level) (Consumed Magic Power)
- Add magic to your own database.
- Save as a string name
- Magic description : stored in str format
- Magic category : select from the list inside spell_choices and save as a string
- Enter a number from 1 to 10 for proficiency. Store in int format
- Consuming horsepower : stored in int format
### / Status Window
- Arguments : /status window
- View the status window you registered.
- (If none are found, return "No registered character information." visible only to the user.)
- Status window list : name, gender, age, dormitory, grade, available magic, and proficiency level (LV)
### / Remaining Magic Power
- Arguments : /remaining magic power
- Check your remaining magical power.
- (If none are found, return "No registered character information." visible only to the user.)
### /Magic Power Settings
- Arguments : /Magic power setting (remaining magic power) (maximum magic power)
- Set your own magic status.
- (If there is no character, return "No registered character information found," visible only to the user.)
### /Mana Recovery
- Arguments : /magic recovery (count: default 1)
- Recovers your magic power. (Subtract if the value is negative)
- (If no magic is set, return "No magic is currently set" visible to the user.)
- Return : (Previous magic / Maximum magic) -> (Current magic / Maximum magic)
### /Magic Removal
- Arguments : /delete-magic (name of the magic)
- Delete one of your spells.
- Magic names are auto-completed up to the top 25 you own.
- (If the magic is not held, return "No registered magic." visible only to the user.)
### /Magic Query
- Arguments : /magic-query (magic name)
- View one of your spells.
- Magic names are auto-completed up to the top 25 you own.
- (If the magic is not held, return "No registered magic." visible only to the user.)
- Return : Magic name, description, category, proficiency, consumed mana
### /Magic Use
- Arguments : /magic_use (magic name)
- Use one of your spells.
- Magic names are auto-completed up to the top 25 you own.
- (If the magic is not held, return "No registered magic." visible only to the user.)
- Decrease your current magic power by the amount of (consumed mana) registered for the spells used.
- (If no magic is set, return "No magic is currently set" visible to the user.)
- (If magic power is low, return "Insufficient (amount of MP).")
- Return : "Magic Name" (reply), "MP Used, Magic Result" (reply)
### / Consumable Power Adjustment
- Arguments : /mana-adjust (magical name) (mana cost)
- Adjusts the mana cost of one of your spells.
- Magic names are auto-completed up to the top 25 you own.
- (If the magic is not held, return "No registered magic." visible only to the user.)
### /Magic Proficiency Adjustment
- Arguments : /Magic Proficiency Adjustment (Magic Name) (Consumed Magic Power)
- Adjusts the proficiency of one of your spells.
- Magic names are auto-completed up to the top 25 you own.
- (If the magic is not held, return "No registered magic." visible only to the user.)
---
## database
    magic_point
    | user's discord id | points | max_points |

    status
    | user's discord id | character_name | sex | age | dormitory | grade |

    user_spells
    | user's discord id | spells(json) |
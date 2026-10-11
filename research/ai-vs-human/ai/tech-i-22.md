# Transaction Isolation Level

## 1. 개요

**트랜잭션 격리 수준(Isolation Level)**은 여러 트랜잭션이 동시에 실행될 때 한 트랜잭션이 다른 트랜잭션의 변경 내용을 어디까지 볼 수 있는지 정하는 기준입니다. ACID 중 **I(Isolation)**를 얼마나 엄격하게 지킬지 정하는 설정이라고 보면 됩니다.

- 격리 수준이 높을수록 데이터 정합성이 좋아지지만 **동시성 처리 성능은 떨어집니다**.
- 격리 수준이 낮을수록 성능은 좋아지지만 **이상 현상(Anomaly)**이 생길 수 있습니다.

ANSI SQL 표준은 네 가지 격리 수준을 정의합니다.

---

## 2. 동시성 이상 현상

### Dirty Read
커밋되지 않은 다른 트랜잭션의 변경 내용을 읽는 현상입니다. 그 트랜잭션이 롤백되면 존재하지 않는 데이터를 읽은 셈이 됩니다.

### Non-Repeatable Read
한 트랜잭션 안에서 같은 행을 두 번 조회했는데, 그 사이 다른 트랜잭션이 해당 행을 **수정(UPDATE)하고 커밋**해서 결과가 달라지는 현상입니다.

### Phantom Read
한 트랜잭션 안에서 같은 조건으로 범위 조회를 두 번 했는데, 그 사이 다른 트랜잭션이 **INSERT/DELETE**를 해서 없던 행이 생기거나 있던 행이 사라지는 현상입니다.

---

## 3. 격리 수준별 정리

| 격리 수준 | Dirty Read | Non-Repeatable Read | Phantom Read |
|---|---|---|---|
| READ UNCOMMITTED | 발생 | 발생 | 발생 |
| READ COMMITTED | 방지 | 발생 | 발생 |
| REPEATABLE READ | 방지 | 방지 | 발생 (표준 기준) |
| SERIALIZABLE | 방지 | 방지 | 방지 |

### READ UNCOMMITTED
- 커밋되지 않은 데이터까지 읽습니다.
- 정합성 문제가 심해서 실무에서는 거의 쓰지 않습니다.

### READ COMMITTED
- 커밋된 데이터만 읽습니다.
- **Oracle, PostgreSQL, SQL Server의 기본값**입니다.
- MVCC 환경에서는 **쿼리(SELECT)마다 새 스냅샷**을 만들기 때문에 Non-Repeatable Read가 발생합니다.

### REPEATABLE READ
- 트랜잭션이 시작된 뒤 처음 읽은 시점의 스냅샷을 끝까지 유지합니다.
- **MySQL InnoDB의 기본값**입니다.
- InnoDB는 일반 SELECT(Consistent Read)에서는 MVCC 스냅샷으로, 잠금 읽기(`SELECT ... FOR UPDATE`)에서는 **Next-Key Lock(Record Lock + Gap Lock)**으로 대부분의 Phantom Read를 막습니다.

### SERIALIZABLE
- 트랜잭션들이 순서대로 하나씩 실행된 것과 같은 결과를 보장합니다.
- InnoDB는 일반 SELECT도 공유 잠금(S Lock)을 거는 방식으로 동작해서 동시성이 크게 떨어집니다.
- PostgreSQL은 **SSI(Serializable Snapshot Isolation)**로 충돌을 감지하고, 충돌이 나면 트랜잭션을 실패시킵니다(재시도 필요).

---

## 4. MVCC와 Undo Log

**MVCC(Multi-Version Concurrency Control)**는 데이터를 변경할 때 이전 버전을 Undo 영역에 보관하고, 각 트랜잭션이 자기 시점에 맞는 버전을 읽게 하는 방식입니다.

- 읽기와 쓰기가 서로를 막지 않아서 동시성이 높습니다.
- READ COMMITTED와 REPEATABLE READ의 차이는 **스냅샷(Read View)을 언제 만드느냐**입니다.
  - RC: SELECT 문마다 새로 만듭니다.
  - RR: 트랜잭션의 첫 SELECT 시점에 한 번 만듭니다.

---

## 5. 추가로 알아둘 이상 현상

- **Lost Update**: 두 트랜잭션이 같은 값을 읽고 각자 수정하면 한쪽 변경이 덮어써지는 현상입니다. 해결 방법은 `SELECT ... FOR UPDATE`, 낙관적 락(버전 컬럼), 원자적 UPDATE(`SET cnt = cnt + 1`)입니다.
- **Write Skew**: 두 트랜잭션이 같은 조건을 읽고 서로 다른 행을 수정해서 전체 제약이 깨지는 현상입니다. 예: 당직 의사가 최소 1명 있어야 하는데 둘 다 동시에 빠지는 경우. Snapshot Isolation으로는 막을 수 없고 SERIALIZABLE이나 명시적 락이 필요합니다.

---

## 6. 면접 예상 질문

**Q1. 격리 수준을 높이면 무조건 좋은가요?**
아닙니다. 잠금 범위와 대기가 늘어나 처리량이 떨어지고 데드락 가능성도 커집니다. 업무 특성에 맞춰 정합성과 성능 사이에서 균형을 잡아야 합니다.

**Q2. MySQL의 기본 격리 수준과 Phantom Read 처리 방식은?**
기본값은 REPEATABLE READ입니다. 일반 조회는 MVCC 스냅샷으로, 잠금 조회는 Gap Lock을 포함한 Next-Key Lock으로 Phantom Read를 대부분 막습니다. 다만 일반 SELECT와 잠금 읽기를 섞어 쓰면 Phantom이 보일 수 있습니다.

**Q3. Spring에서는 어떻게 설정하나요?**
`@Transactional(isolation = Isolation.READ_COMMITTED)`처럼 지정합니다. `DEFAULT`는 DB의 기본 격리 수준을 따릅니다.

**Q4. 실무에서 READ COMMITTED를 쓰는 이유는?**
Gap Lock이 없어서 잠금 경합과 데드락이 줄어들고, 대부분의 OLTP 업무에서는 이 정도 정합성으로 충분하기 때문입니다. 대신 정합성이 중요한 구간은 명시적 락이나 낙관적 락으로 보완합니다.

---

## 7. 한 줄 요약

> 격리 수준은 **정합성과 동시성 사이의 트레이드오프**입니다. 각 수준이 어떤 이상 현상을 허용하는지, 그리고 MVCC와 락으로 어떻게 구현되는지를 함께 설명할 수 있어야 합니다.

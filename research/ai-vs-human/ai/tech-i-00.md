# Semaphore & Mutex

## 1. 개요
여러 스레드(또는 프로세스)가 공유 자원에 동시에 접근하면 실행 순서에 따라 결과가 달라지는 **경쟁 조건(Race Condition)**이 생깁니다. Mutex와 Semaphore는 이런 상황을 막기 위한 대표적인 **동기화(Synchronization) 도구**입니다.

## 2. Mutex (Mutual Exclusion, 상호 배제)
- 한 번에 **하나의 스레드만** 임계 영역(Critical Section)에 들어갈 수 있도록 보장합니다.
- **소유권(Ownership)** 개념이 있습니다. lock을 획득한 스레드만 unlock할 수 있습니다.
- 같은 스레드가 다시 lock을 잡는 **재진입(Reentrant)** 을 허용할지는 구현에 따라 다릅니다.
- 예: `pthread_mutex_t`, C++ `std::mutex`, Java `ReentrantLock`

```python
import threading

lock = threading.Lock()
counter = 0

def increment():
    global counter
    with lock:          # 임계 영역 진입
        counter += 1    # 한 번에 한 스레드만 실행
```

## 3. Semaphore (세마포어)
- Dijkstra가 제안한 **카운터 기반 신호 메커니즘**입니다.
- 두 가지 연산이 있습니다.
  - **P (wait / acquire)**: 카운터가 0보다 크면 1 감소시키고 진입, 아니면 대기
  - **V (signal / release)**: 카운터를 1 증가시키고 대기 중인 스레드를 깨움
- 카운터 값 N은 **동시에 N개까지 접근을 허용**한다는 뜻입니다.
- **이진 세마포어(0/1)** 와 **계수 세마포어(0~N)** 로 나뉩니다.
- **소유권이 없습니다.** 획득한 스레드가 아닌 다른 스레드도 release할 수 있습니다.
- 예: 커넥션 풀 크기 제한, 동시 요청 수 제한, 생산자-소비자 문제의 버퍼 관리

## 4. 비교 정리

| 구분 | Mutex | Semaphore |
|---|---|---|
| 허용 수 | 1 | N (0~N) |
| 소유권 | 있음 | 없음 |
| 주된 목적 | 상호 배제 | 자원 개수 제어, 스레드 간 신호 |
| 재진입 | 구현에 따라 가능 | 해당 없음 |
| 해제 주체 | 획득한 스레드만 | 아무 스레드나 가능 |

## 5. 면접 핵심 포인트
- **Q. Mutex와 Semaphore의 차이는?**
  A. Mutex는 소유권이 있는 상호 배제 도구이고, Semaphore는 카운터로 동시 접근 수를 제어하는 신호 도구입니다.
- **Q. 이진 세마포어로 Mutex를 대신할 수 있나요?**
  A. 동작은 가능하지만 소유권이 없어 실수로 다른 스레드가 release하면 문제가 생깁니다. 또한 우선순위 역전 방지 기능도 없으므로 상호 배제 목적이라면 Mutex를 쓰는 것이 권장됩니다.
- **Q. 데드락의 4가지 necessary condition은?**
  A. 상호 배제, 점유와 대기, 비선점, 순환 대기입니다. 이 중 하나라도 깨면 데드락을 예방할 수 있습니다. 예를 들어 자원 획득 순서를 일정하게 정하면 순환 대기를 막을 수 있습니다.

## 6. 한 줄 요약
> **Mutex는 "한 명만 들어가는 화장실 열쇠"**, **Semaphore는 "N개의 주차 자리"** 로 기억하면 편합니다.

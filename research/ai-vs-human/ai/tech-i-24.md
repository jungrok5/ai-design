# Composite Pattern

## 핵심 개념
Composite 패턴은 객체들을 **트리 구조**로 묶어, 개별 객체(부분)와 객체 묶음(전체)을 **동일한 인터페이스**로 다루게 하는 구조 설계 패턴입니다. 클라이언트는 대상이 단일 객체인지 복합 객체인지 신경 쓰지 않고 같은 방식으로 연산을 호출할 수 있습니다.

## 구성 요소
- **Component**: Leaf와 Composite가 공유하는 공통 인터페이스입니다. (예: `size()`, `draw()`)
- **Leaf**: 자식이 없는 기본 객체이며, 실제 작업을 직접 수행합니다.
- **Composite**: 여러 Component를 자식으로 보관합니다. 연산을 자식들에게 위임한 뒤 결과를 합칩니다.

## 예시 (Python)
```python
from abc import ABC, abstractmethod

class Node(ABC):
    @abstractmethod
    def size(self) -> int: ...

class File(Node):                      # Leaf
    def __init__(self, size: int):
        self._size = size
    def size(self) -> int:
        return self._size

class Directory(Node):                 # Composite
    def __init__(self):
        self._children: list[Node] = []
    def add(self, node: Node):
        self._children.append(node)
    def size(self) -> int:
        return sum(child.size() for child in self._children)
```
클라이언트는 `File`과 `Directory`를 구분하지 않고 `size()`만 호출하면 됩니다. 재귀적으로 전체 크기가 계산됩니다.

## 장점
- 재귀 구조를 조건문 없이 단순하게 처리할 수 있습니다.
- 새로운 Component 종류를 추가해도 기존 클라이언트 코드를 거의 수정하지 않아도 됩니다. (개방-폐쇄 원칙)

## 단점
- 리프와 복합체의 차이가 중요한 경우 설계가 어색해집니다. 예를 들어 `add()`를 Leaf에서 어떻게 처리할지 고민해야 합니다.
- 트리 구조의 제약(예: 특정 노드에 특정 자식만 허용)을 타입 시스템으로 강제하기 어렵습니다.

## 실제 적용 사례
GUI 위젯 트리(Window → Panel → Button), 파일 시스템, 조직도, 수식 AST, 브라우저 DOM 등이 대표적입니다.

## 면접 대비 포인트
- **Composite vs Decorator**: Composite는 여러 자식으로 이루어진 트리 구조를 다루고, Decorator는 하나의 객체에 기능을 덧씌우는 구조를 다룹니다.
- **투명성 vs 안전성**: `add()` 같은 자식 관리 메서드를 Component에 선언하면 클라이언트가 동일하게 쓸 수 있지만(투명성), Leaf에서 예외를 던져야 합니다. Composite에만 선언하면 타입 안전성은 높아지지만 클라이언트가 타입을 구분해야 합니다(안전성).
- **순회**: 트리를 순회할 때는 Iterator나 Visitor 패턴과 함께 쓰이는 경우가 많습니다.

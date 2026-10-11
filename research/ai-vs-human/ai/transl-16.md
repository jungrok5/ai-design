# HTTP 캐싱

**HTTP 캐싱**은 이전에 가져온 리소스를 저장해 두었다가 재사용함으로써 응답 속도를 높이고 네트워크 사용량과 서버 부하를 줄이는 기법입니다. 캐시는 요청과 응답 사이에 위치하여, 요청된 URL에 대응하는 응답이 저장되어 있으면 원본 서버에 가지 않고 그 사본을 돌려줍니다.

## 캐시의 종류

HTTP 캐시는 저장 위치와 공유 범위에 따라 크게 두 가지로 나뉩니다.

### 개인 캐시 (Private cache)

개인 캐시는 단일 사용자에게 할당된 캐시로, 대부분 브라우저 안에 존재합니다. 브라우저에서 "뒤로 가기"를 눌렀을 때 페이지가 즉시 나타나거나, 이미 내려받은 이미지가 다시 요청되지 않는 것은 이 캐시 덕분입니다. 개인 캐시에는 해당 사용자만을 위한 개인화된 응답을 저장해도 안전합니다.

```http
Cache-Control: private
```

### 공유 캐시 (Shared cache)

공유 캐시는 클라이언트와 서버 사이에 위치하며, 여러 사용자가 재사용할 수 있는 응답을 저장합니다. 프록시 서버, CDN(콘텐츠 전송 네트워크), 리버스 프록시 등이 여기에 속합니다. 사용자별 응답이 공유 캐시에 저장되면 다른 사용자에게 노출될 수 있으므로 주의해야 합니다.

```http
Cache-Control: public, max-age=3600
```

## 캐시 대상

HTTP 캐시는 원칙적으로 `GET` 요청에 대한 `200 OK` 응답을 주로 저장합니다. 그 밖에 `301 Moved Permanently` 같은 영구 리디렉션, `404 Not Found` 같은 오류 응답, `206 Partial Content` 응답 등도 조건에 따라 저장될 수 있습니다. `POST`처럼 서버 상태를 변경하는 메서드의 응답은 일반적으로 캐시하지 않지만, 명시적인 신선도 정보가 있고 `Content-Location` 헤더가 함께 있는 경우 등 예외가 있습니다.

## Cache-Control 헤더

`Cache-Control` 헤더는 요청과 응답 모두에서 캐시 동작을 지시하는 핵심 수단입니다.

| 지시어 | 설명 |
| --- | --- |
| `max-age=N` | 응답이 생성된 시점부터 N초 동안 신선한 것으로 간주합니다. |
| `s-maxage=N` | 공유 캐시에만 적용되는 `max-age`입니다. |
| `no-cache` | 저장은 가능하지만 사용 전에 반드시 원본 서버에 검증해야 합니다. |
| `no-store` | 어떤 캐시에도 응답을 저장하지 않습니다. |
| `must-revalidate` | 신선도가 만료된 후에는 반드시 재검증해야 하며, 오래된 응답을 사용할 수 없습니다. |
| `public` | 공유 캐시를 포함해 어디에든 저장할 수 있습니다. |
| `private` | 개인 캐시에만 저장할 수 있습니다. |
| `immutable` | 신선한 동안 리소스가 변경되지 않으므로 재검증이 필요 없음을 나타냅니다. |

흔히 혼동하는 점은 `no-cache`가 "캐시하지 않음"을 뜻하지 않는다는 것입니다. 캐시하지 않으려면 `no-store`를 사용해야 합니다.

## 신선도와 만료

저장된 응답은 **신선(fresh)** 상태와 **오래됨(stale)** 상태를 가집니다. 신선한 응답은 서버에 묻지 않고 곧바로 재사용할 수 있습니다. 신선 기간은 다음 순서로 결정됩니다.

1. `Cache-Control: s-maxage` (공유 캐시) 또는 `max-age`
2. `Expires` 헤더 (특정 날짜까지 유효)
3. 둘 다 없으면 `Last-Modified`를 기반으로 한 휴리스틱 계산

응답이 캐시에 머문 시간은 `Age` 헤더로 확인할 수 있습니다. `Age`가 `max-age`보다 작으면 응답은 아직 신선합니다.

```http
HTTP/1.1 200 OK
Cache-Control: max-age=604800
Age: 120
```

위 응답은 7일 동안 신선하며, 현재 120초가 지난 상태입니다.

## 검증 (Validation)

응답이 오래된 상태가 되면 캐시는 곧바로 버리지 않고 원본 서버에 **조건부 요청**을 보내 여전히 유효한지 확인합니다. 리소스가 바뀌지 않았다면 서버는 본문 없이 `304 Not Modified`를 응답하고, 캐시는 저장된 사본의 신선도를 갱신하여 계속 사용합니다. 이렇게 하면 본문 전송 비용을 아낄 수 있습니다.

### ETag와 If-None-Match

`ETag`는 리소스의 특정 버전을 식별하는 값입니다. 클라이언트는 이 값을 `If-None-Match`에 담아 보냅니다.

```http
GET /style.css HTTP/1.1
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```

값이 일치하면 서버는 `304 Not Modified`를 반환합니다.

### Last-Modified와 If-Modified-Since

`Last-Modified`는 리소스의 마지막 수정 시각을 나타냅니다. 클라이언트는 `If-Modified-Since`로 해당 시각 이후에 변경되었는지 묻습니다. `ETag`가 더 정밀하므로 둘이 함께 있으면 `ETag`가 우선합니다.

## 캐시 무효화와 버전 관리

한 번 캐시된 리소스는 신선 기간 동안 서버가 바꾸어도 클라이언트에 반영되지 않습니다. 이를 해결하는 대표적인 방법이 **리비전된 URL(캐시 버스팅)** 입니다. 파일 내용이 바뀔 때마다 URL에 해시나 버전을 넣어 새로운 리소스로 취급되게 하는 방식입니다.

```html
<link rel="stylesheet" href="/assets/app.3f9a1c.css" />
```

이 방식에서는 정적 자산에 매우 긴 수명과 `immutable`을 지정하고, HTML 문서는 짧은 수명이나 `no-cache`로 두어 항상 최신 자산 URL을 참조하게 합니다.

```http
Cache-Control: public, max-age=31536000, immutable
```

## Vary 헤더

같은 URL이라도 요청 헤더에 따라 응답이 달라질 수 있습니다. 예를 들어 `Accept-Encoding`에 따라 압축 방식이 다르다면, 캐시는 이를 구분해서 저장해야 합니다. `Vary` 헤더는 응답 선택에 사용된 요청 헤더를 지정합니다.

```http
Vary: Accept-Encoding, Accept-Language
```

`Vary: *`는 사실상 캐시된 응답을 재사용할 수 없음을 의미합니다.

## 오래된 응답의 활용

최신 지시어를 사용하면 오래된 응답을 안전하게 활용할 수도 있습니다.

- `stale-while-revalidate=N`: 만료 후 N초 동안은 오래된 응답을 즉시 반환하고, 백그라운드에서 새로 검증합니다.
- `stale-if-error=N`: 원본 서버에 오류가 발생했을 때 N초 동안 오래된 응답을 대신 사용합니다.

```http
Cache-Control: max-age=600, stale-while-revalidate=300
```

## 모범 사례

- 변경되지 않는 정적 자산은 해시가 포함된 URL과 함께 긴 `max-age`를 사용하세요.
- 자주 바뀌는 HTML은 `no-cache`와 `ETag`를 조합해 항상 재검증하세요.
- 개인 정보나 민감한 데이터는 `no-store` 또는 `private`을 지정하세요.
- 응답이 요청 헤더에 따라 달라진다면 `Vary`를 정확히 설정하세요.
- 캐시 동작은 개발자 도구의 네트워크 탭에서 `Age`, `Cache-Control`, 상태 코드(`304` 등)로 확인하세요.

## 같이 보기

- [`Cache-Control`](https://developer.mozilla.org/ko/docs/Web/HTTP/Headers/Cache-Control) 헤더
- [`ETag`](https://developer.mozilla.org/ko/docs/Web/HTTP/Headers/ETag) 헤더
- [`Vary`](https://developer.mozilla.org/ko/docs/Web/HTTP/Headers/Vary) 헤더
- [HTTP 조건부 요청](https://developer.mozilla.org/ko/docs/Web/HTTP/Conditional_requests)

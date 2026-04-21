# 旅遊系統 - 路由設計文件 (ROUTES)

本文件依據 PRD 與 ARCHITECTURE 確立系統的路由 (Routes) 結構，並定義網址路徑、前端模板的對應關係與基本邏輯，供後續實作對齊。

## 1. 路由總覽表格

| 功能模組 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁** | GET | `/` | `templates/index.html` | 顯示首頁畫面與搜尋列 |
| **搜尋景點** | GET | `/search` | `templates/search.html` | 顯示符合搜尋關鍵字的景點列表 |
| **景點詳情與天氣** | GET | `/places/<id>` | `templates/detail.html` | 顯示該景點的介紹、圖片與即時天氣預報 |
| **景點周邊餐廳** | GET | `/places/<id>/restaurants` | `templates/restaurants.html` | 顯示該景點附近的餐廳與美食列表 |
| **行程列表** | GET | `/plan` | `templates/planner_list.html` | 顯示使用者現有的所有行程總表 (Itinerary) |
| **建立行程頁面** | GET | `/plan/new` | `templates/planner_new.html` | 填寫新行程名稱與日期的表單頁面 |
| **儲存新行程** | POST | `/plan/create` | — | 接收建立行程表單，寫入資料庫後重導向至 `/plan` |
| **行程細項規劃** | GET | `/plan/<itinerary_id>` | `templates/planner_detail.html` | 顯示該行程內目前排定的景點與餐廳列表 |
| **新增項目至行程**| POST | `/plan/<itinerary_id>/items/add` | — | 接收從景點或餐廳頁面送出的表單，加入清單後重導向 |
| **刪除行程項目** | POST | `/plan/<itinerary_id>/items/<item_id>/delete`| — | 從行程表移除特定項目後，重導向回行程細項頁面 |

---

## 2. 每個路由的詳細說明

### `main.py` (首頁與搜尋)
- **`GET /`**
  - 輸入：無
  - 處理邏輯：單純回傳首頁。
  - 輸出：渲染 `index.html`
- **`GET /search`**
  - 輸入：URL Query Parameter `?q=` (關鍵字)
  - 處理邏輯：呼叫 `Attraction.get_all()` (實作時可擴充 where like 篩選)。
  - 輸出：渲染 `search.html`，傳入 `attractions` 清單。
  - 錯誤處理：若無結果，則回傳空陣列並顯示提示字眼。

### `places.py` (景點與餐廳)
- **`GET /places/<id>`**
  - 輸入：景點 ID
  - 處理邏輯：
    1. 呼叫 `Attraction.get_by_id(id)`。
    2. 呼叫外部天氣 API (如 OpenWeatherMap)，取得該 location 的天氣。
  - 輸出：渲染 `detail.html`，傳入 `attraction` 與 `weather_info`。
  - 錯誤處理：若找不到 ID 則回傳 404。
- **`GET /places/<id>/restaurants`**
  - 輸入：景點 ID
  - 處理邏輯：確認景點存在後，呼叫 `Restaurant.get_by_attraction_id(id)`。
  - 輸出：渲染 `restaurants.html`，傳入 `restaurants` 與景點資訊。

### `plan.py` (行程規劃)
- **`GET /plan`**
  - 輸入：無
  - 處理邏輯：呼叫 `Itinerary.get_all()` 獲取清單。
  - 輸出：渲染 `planner_list.html`。
- **`GET /plan/new`**
  - 處理邏輯：簡單渲染表單頁。
  - 輸出：渲染 `planner_new.html`。
- **`POST /plan/create`**
  - 輸入：`title` Form Data
  - 處理邏輯：呼叫 `Itinerary.create(...)` 並取得新增的 ID。
  - 輸出：重導向 `redirect('/plan')`。
- **`GET /plan/<itinerary_id>`**
  - 輸入：行程總表 ID
  - 處理邏輯：呼叫 `ItineraryItem.get_by_itinerary_id()`，並關聯查詢詳細名稱。
  - 輸出：渲染 `planner_detail.html`。
- **`POST /plan/<itinerary_id>/items/add`**
  - 輸入：`item_type`, `item_id`, `event_time` Form Data
  - 處理邏輯：呼叫 `ItineraryItem.create(...)` 存入指定行程。
  - 輸出：重導向回 `redirect('/plan/<itinerary_id>')` 或 `redirect` 來源頁面。
- **`POST /plan/<itinerary_id>/items/<item_id>/delete`**
  - 輸入：行程項目 ID (`item_id`)
  - 處理邏輯：呼叫 `ItineraryItem.delete(item_id)` 刪除紀錄。
  - 輸出：重導向回 `redirect('/plan/<itinerary_id>')`。

---

## 3. Jinja2 模板清單

以下是計畫建立的 HTML 模板檔案，全部繼承自相同的 `base.html` 來共用 Navigation 與 CSS：

* `templates/base.html` (根模板，包含 header, footer, viewport 與靜態檔載入)
* `templates/index.html` (首頁搜尋畫面)
* `templates/search.html` (搜尋結果列表)
* `templates/detail.html` (景點詳情、圖片與天氣呈現)
* `templates/restaurants.html` (周邊餐廳列表)
* `templates/planner_list.html` (所有行程專案一覽表)
* `templates/planner_new.html` (建立新行程專案的簡易表單)
* `templates/planner_detail.html` (時間軸形式呈現已排定的行程明細)

---

## 4. 路由骨架程式碼
程式碼皆已生成於 `app/routes/` 之下，套用了 Flask 的 `Blueprint` 機制來分離管理。

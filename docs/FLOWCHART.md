# 旅遊系統 - 流程圖文件 (FLOWCHART)

這份文件基於 `docs/PRD.md` 的功能需求與 `docs/ARCHITECTURE.md` 的系統架構，描述了使用者的操作流程與系統內部的運作機制。

## 1. 使用者流程圖 (User Flow)

此流程圖展示了年輕旅行者進入旅遊平台後，主要能夠進行的操作路徑，包含搜尋、檢視景點與天氣、搜尋周邊餐廳，到最後的行程規劃。

```mermaid
flowchart LR
    A([使用者造訪首頁]) --> B{想做什麼？}
    
    B -->|搜尋旅遊資訊| C[輸入地區或關鍵字進行搜尋]
    C --> D[搜尋結果列表]
    
    D -->|點擊景點| E[景點詳細介紹與天氣頁面]
    E -->|查看當地天氣| F[顯示穿搭建議與天氣預報]
    E -->|找附近美食| G[顯示周邊推薦餐廳與資訊]
    
    B -->|規劃旅遊行程| H[開啟行程規劃表]
    D -->|加入行程| H
    E -->|加入行程| H
    G -->|加入行程| H
    
    H --> I[編輯/拖排日期與時間]
    I --> J([完成個人專屬旅遊行程])
```

## 2. 系統序列圖 (Sequence Diagram)

此圖以「使用者透過搜尋功能查看景點並規劃行程」為例，展示前端瀏覽器、Flask 後端、外部天氣 API 與 SQLite 資料庫之間的互動順序。

```mermaid
sequenceDiagram
    actor User as 年輕旅行者
    participant Browser as 瀏覽器 (前端)
    participant Route as Flask Route
    participant Weather as 外部天氣 API
    participant Model as Data Model
    participant DB as SQLite

    %% 步驟 1: 搜尋與查看景點
    User->>Browser: 搜尋地區並點選特定景點
    Browser->>Route: GET /places/<id>
    Route->>Model: 依據 ID 查詢景點與餐廳
    Model->>DB: SELECT 景點與周邊餐廳資料
    DB-->>Model: 回傳資料紀錄
    Model-->>Route: 回傳 Python 物件
    Route->>Weather: GET 天氣資訊 (依據景點座標)
    Weather-->>Route: 回傳即時天氣 JSON 資料
    Route-->>Browser: 渲染 detail.html 並回傳
    Browser-->>User: 顯示景點詳細、天氣與周邊餐廳

    %% 步驟 2: 加入行程並規劃
    User->>Browser: 點選「加入行程」並設定日期時間
    Browser->>Route: POST /plan/add
    Route->>Model: 驗證資料並呼叫新增邏輯
    Model->>DB: INSERT INTO itinerary
    DB-->>Model: 新增成功
    Model-->>Route: 建立成功狀態
    Route-->>Browser: 302 重導向至 /plan
    Browser->>Route: GET /plan 
    Route->>Model: 讀取使用者的所有行程清單
    Model->>DB: SELECT * FROM itinerary
    DB-->>Model: 回傳所有行程紀錄
    Model-->>Route: 回傳 Python 列表
    Route-->>Browser: 渲染 planner.html 並回傳
    Browser-->>User: 顯示排好的專屬行程表
```

## 3. 功能清單對照表

以下為統整出的主要功能、對應的獨立 URL 路徑與 HTTP 方法的介面規劃總表：

| 主要功能 | 說明 | HTTP 方法 | URL 路徑 (暫定) |
| --- | --- | --- | --- |
| **首頁** | 顯示系統進入畫面與搜尋框 | GET | `/` |
| **搜尋功能** | 處理搜尋關鍵字，回傳符合的結果列表 | GET | `/search` |
| **景點查詢與天氣** | 顯示單一景點的完整介紹與動態天氣 | GET | `/places/<id>` |
| **查詢吃飯的地方** | 顯示景點周邊的推薦餐廳清單 | GET | `/places/<id>/restaurants` |
| **查看行程表** | 顯示使用者已規劃好的行程列表 | GET | `/plan` |
| **新增/規劃行程** | 將景點或餐廳寫入使用者的行程規劃內 | POST | `/plan/add` |
| **編輯/刪除行程** | 變更時間或從規劃清單中移除特定項目 | POST | `/plan/update_or_delete` |

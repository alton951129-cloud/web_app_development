# 旅遊系統 - 系統架構文件 (ARCHITECTURE)

## 1. 技術架構說明

根據本專案的需求與技術限制，我們選擇以下技術來建構旅遊系統：

- **後端框架：Python + Flask**
  - **原因**：Flask 是一套輕量級的 Web 框架，學習曲線平緩且非常靈活，適合用來快速開發 MVP（最小可行性產品）。
- **模板引擎：Jinja2**
  - **原因**：與 Flask 完美整合，能夠在伺服器端將後端的動態資料注入到 HTML 中，直接渲染出完整的網頁傳送給瀏覽器。
- **資料庫：SQLite**
  - **原因**：無需額外安裝獨立的資料庫伺服器，資料儲存在單一檔案中，部署與移轉方便，滿足初期系統的輕量級資料儲存需求。

### Flask MVC 模式說明
本專案採用類似經典 MVC (Model-View-Controller) 的架構模式來組織程式碼：
- **Model (資料模型)**：負責與 SQLite 資料庫溝通，處理景點、餐廳、行程等資料的存取與邏輯運算。
- **View (視圖)**：負責呈現使用者介面。在這個專案中，由 Jinja2 HTML 模板加上 CSS/JS 構成，用來展示從後端傳遞過來的資料。
- **Controller (控制器)**：由 Flask 的路由處理函式（Routes）擔任。負責接收來自瀏覽器的請求，呼叫對應的 Model 取得資料，最後將資料傳遞給 Jinja2 View 進行網頁渲染。

## 2. 專案資料夾結構

以下是本系統的資料夾結構與相對應職責：

```text
web_app_development/
├── app/                  # 應用程式主要資料夾
│   ├── models/           # (Model) 資料庫存取層、定義與 SQLite 互動的邏輯
│   │   ├── __init__.py
│   │   ├── attraction.py # 景點資料模型
│   │   ├── restaurant.py # 餐廳資料模型
│   │   └── itinerary.py  # 行程資料模型
│   ├── routes/           # (Controller) Flask 路由，處理 HTTP 請求
│   │   ├── __init__.py
│   │   ├── main.py       # 首頁與基礎搜尋路由
│   │   ├── places.py     # 景點與餐廳相關路由
│   │   └── plan.py       # 行程規劃相關路由
│   ├── templates/        # (View) Jinja2 HTML 模板檔案
│   │   ├── base.html     # 共用版型 (Header, Footer, Navigation)
│   │   ├── index.html    # 首頁 (包含搜尋框)
│   │   ├── search.html   # 搜尋結果頁
│   │   ├── detail.html   # 景點/餐廳介紹與天氣資訊頁
│   │   └── planner.html  # 行程規劃頁
│   └── static/           # 靜態資源檔案
│       ├── css/          # 樣式表 (包含 Mobile-First 設計)
│       ├── js/           # 網頁互動腳本
│       └── images/       # 圖片與圖示資源
├── instance/             # 存放變動性或機密的系統狀態檔案
│   └── database.db       # SQLite 實體資料庫檔案 
├── docs/                 # 專案說明文件 (包含 PRD, ARCHITECTURE 等)
├── .gitignore            # Git 忽略設定擋
├── requirements.txt      # 紀錄所需的 Python 套件庫
└── app.py                # 系統執行入口點，啟動 Flask 伺服器
```

## 3. 元件關係圖

以下圖示呈現了系統運作時，各個主要元件之間是如何互動的：

```mermaid
flowchart TD
    Browser[瀏覽器 (使用者)]
    
    subgraph Flask Server [Flask 後端伺服器]
        Route[Flask Route (Controller)]
        Template[Jinja2 Template (View)]
        Model[Data Model (Model)]
    end
    
    DB[(SQLite 資料庫)]
    WeatherAPI[外部天氣 API]

    Browser -- "1. 發送請求 (如: 查詢景點詳細與天氣)" --> Route
    Route -- "2. 詢問外部服務" --> WeatherAPI
    WeatherAPI -- "3. 回傳即時天氣資料" --> Route
    Route -- "4. 請求資料存取" --> Model
    Model -- "5. 查詢 / 寫入資料" --> DB
    DB -- "6. 回傳資料結果" --> Model
    Model -- "7. 回傳 Python 物件" --> Route
    Route -- "8. 傳入組合完畢的資料 (Context)" --> Template
    Template -- "9. 渲染成 HTML 結構" --> Route
    Route -- "10. 將 HTML 回應給使用者" --> Browser
```

## 4. 關鍵設計決策

1. **採用伺服器渲染 (SSR) 而非前後端分離 API 架構**
   - **原因**：為了快速交付 MVP，使用 Flask 搭配 Jinja2 能夠大幅減少前端狀態管理與 API 串接的複雜度。這能讓團隊成員快速預覽並且符合基礎的 SEO 要求。
2. **行動裝置優先 (Mobile-First) 的介面開發策略**
   - **原因**：根據 PRD，目標用戶年輕族群高度依賴手機。因此，網頁樣式撰寫將從小螢幕出發，確保手機上能獲得最佳的「找景點、排行程」體驗，再向平板或桌機擴展 (RWD)。
3. **整合外部天氣 API 即時查詢**
   - **原因**：天氣資訊具有強烈的時效性，我們決定在使用者訪問需要天氣資訊的頁面（例如行程規劃或景點詳情）時，由 Flask Route 動態呼叫外部服務（如 OpenWeatherMap API），確保年輕旅行者得到的資訊是最新的，無需自己維護天氣資料庫。
4. **單一資料庫配置 (SQLite)**
   - **原因**：考慮到行程規劃與景點查詢並未涉及大量高併發寫入，SQLite 提供的本地檔案系統存取能力足以滿足初期流量需求，且不需要架設額外的 Database Server 以減少維護成本。未來若需要升級可再無痛轉移至 PostgreSQL。

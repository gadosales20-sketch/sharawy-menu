from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# قائمة لتخزين الطلبات في ذاكرة السيرفر
orders_db = []

HTML_MENU = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <meta name="description" content="مطعم الشعراوي - قائمة الطعام الرقمية." />
  <meta name="theme-color" content="#0f0f0f" />
  <title>الشعراوي | Sharawy Digital Menu</title>
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23e85d04'/%3E%3Ctext x='50' y='68' font-size='55' text-anchor='middle' fill='white' font-family='Arial'%3Eش%3C/text%3E%3C/svg%3E" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #e85d04;
      --primary-dark: #d00000;
      --bg-dark: #0f0f0f;
      --bg-card: #1a1a1a;
      --bg-card-hover: #242424;
      --text: #ffffff;
      --text-muted: #b0b0b0;
      --accent: #ffba08;
      --border: #333;
      --radius: 16px;
      --shadow: 0 8px 24px rgba(0,0,0,0.4);
    }
    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    body { font-family: 'Cairo', sans-serif; background: var(--bg-dark); color: var(--text); min-height: 100vh; padding-bottom: 90px; line-height: 1.5; }
    .header { position: sticky; top: 0; z-index: 100; background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%); border-bottom: 1px solid var(--border); padding: 12px 16px 10px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
    .logo-area { display: flex; align-items: center; gap: 10px; }
    .logo-circle { width: 48px; height: 48px; background: linear-gradient(135deg, var(--primary), var(--primary-dark)); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; box-shadow: 0 4px 12px rgba(232, 93, 4, 0.4); }
    .brand { display: flex; flex-direction: column; }
    .brand-name { font-size: 20px; font-weight: 800; color: var(--text); letter-spacing: -0.5px; }
    .brand-sub { font-size: 11px; color: var(--text-muted); font-weight: 400; }
    .header-actions { display: flex; gap: 8px; }
    .icon-btn { width: 42px; height: 42px; border-radius: 12px; background: var(--bg-card); border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; color: var(--text); font-size: 18px; cursor: pointer; transition: all 0.2s; }
    .icon-btn:active { transform: scale(0.92); background: var(--bg-card-hover); }
    .search-bar { padding: 0 16px 12px; background: #0f0f0f; }
    .search-input { width: 100%; background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 12px 16px 12px 44px; color: var(--text); font-family: inherit; font-size: 15px; outline: none; transition: border-color 0.2s; }
    .search-input:focus { border-color: var(--primary); }
    .search-wrapper { position: relative; }
    .search-icon { position: absolute; right: 16px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 18px; pointer-events: none; }
    .categories { display: flex; gap: 10px; padding: 8px 16px 16px; overflow-x: auto; scrollbar-width: none; }
    .categories::-webkit-scrollbar { display: none; }
    .cat-chip { flex-shrink: 0; padding: 10px 18px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 50px; font-size: 14px; font-weight: 600; color: var(--text-muted); cursor: pointer; transition: all 0.2s; white-space: nowrap; }
    .cat-chip.active { background: linear-gradient(135deg, var(--primary), var(--primary-dark)); border-color: transparent; color: white; box-shadow: 0 4px 14px rgba(232, 93, 4, 0.35); }
    .section { padding: 0 16px 24px; }
    .section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
    .section-title { font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
    .section-title::before { content: ''; width: 4px; height: 20px; background: var(--primary); border-radius: 4px; }
    .products-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .product-card { background: var(--bg-card); border-radius: var(--radius); overflow: hidden; border: 1px solid var(--border); transition: all 0.2s; cursor: pointer; display: flex; flex-direction: column; }
    .product-card:active { transform: scale(0.98); background: var(--bg-card-hover); }
    .product-img { height: 110px; background: linear-gradient(145deg, #2a2a2a, #1f1f1f); display: flex; align-items: center; justify-content: center; font-size: 42px; position: relative; }
    .product-img.combo { background: linear-gradient(145deg, #3d1f00, #1a0f00); }
    .product-body { padding: 12px; flex: 1; display: flex; flex-direction: column; gap: 6px; }
    .product-name { font-size: 14px; font-weight: 700; line-height: 1.3; color: var(--text); }
    .product-desc { font-size: 11px; color: var(--text-muted); line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .product-footer { display: flex; align-items: center; justify-content: space-between; margin-top: auto; padding-top: 8px; }
    .price { font-size: 16px; font-weight: 800; color: var(--accent); }
    .price span { font-size: 11px; font-weight: 500; color: var(--text-muted); margin-right: 2px; }
    .add-btn { width: 34px; height: 34px; border-radius: 10px; background: var(--primary); border: none; color: white; font-size: 20px; font-weight: 700; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.15s; box-shadow: 0 4px 10px rgba(232, 93, 4, 0.3); }
    .offer-card { grid-column: 1 / -1; display: flex; flex-direction: row; height: 120px; }
    .offer-card .product-img { width: 120px; height: 100%; flex-shrink: 0; font-size: 48px; }
    .cart-bar { position: fixed; bottom: 0; left: 0; right: 0; background: linear-gradient(0deg, #1a1a1a 80%, transparent); padding: 16px 16px 24px; z-index: 200; display: none; }
    .cart-bar.visible { display: block; }
    .cart-btn { width: 100%; background: linear-gradient(135deg, var(--primary), var(--primary-dark)); border: none; border-radius: 16px; padding: 16px 20px; color: white; font-family: inherit; font-size: 16px; font-weight: 700; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 8px 24px rgba(232, 93, 4, 0.4); cursor: pointer; }
    .cart-count { background: white; color: var(--primary-dark); width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 800; }
    .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.75); z-index: 300; display: none; align-items: flex-end; justify-content: center; }
    .modal-overlay.open { display: flex; }
    .modal { background: var(--bg-card); width: 100%; max-width: 480px; border-radius: 24px 24px 0 0; max-height: 85vh; overflow-y: auto; padding: 24px 20px 32px; animation: slideUp 0.3s ease; }
    @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
    .modal-handle { width: 40px; height: 4px; background: #444; border-radius: 4px; margin: 0 auto 20px; }
    .modal-img { height: 160px; background: linear-gradient(145deg, #2a2a2a, #1f1f1f); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 64px; margin-bottom: 16px; }
    .modal-title { font-size: 22px; font-weight: 800; margin-bottom: 6px; }
    .modal-price { font-size: 20px; font-weight: 800; color: var(--accent); margin-bottom: 16px; }
    .option-group { margin-bottom: 18px; }
    .option-label { font-size: 14px; font-weight: 700; margin-bottom: 10px; color: var(--text); }
    .options { display: flex; flex-wrap: wrap; gap: 8px; }
    .option { padding: 8px 14px; background: #2a2a2a; border: 1px solid var(--border); border-radius: 10px; font-size: 13px; font-weight: 600; color: var(--text-muted); cursor: pointer; transition: all 0.15s; }
    .option.selected { background: var(--primary); border-color: var(--primary); color: white; }
    .qty-control { display: flex; align-items: center; gap: 16px; margin: 20px 0; }
    .qty-btn { width: 40px; height: 40px; border-radius: 12px; background: #2a2a2a; border: 1px solid var(--border); color: white; font-size: 20px; font-weight: 700; cursor: pointer; }
    .qty-value { font-size: 20px; font-weight: 800; min-width: 30px; text-align: center; }
    .modal-add { width: 100%; padding: 16px; background: linear-gradient(135deg, var(--primary), var(--primary-dark)); border: none; border-radius: 14px; color: white; font-family: inherit; font-size: 16px; font-weight: 700; cursor: pointer; margin-top: 8px; }
    .cart-empty { text-align: center; padding: 50px 20px; color: var(--text-muted); }
    .cart-empty-icon { font-size: 48px; margin-bottom: 12px; }
    .cart-item { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--border); }
    .cart-item-img { width: 52px; height: 52px; flex-shrink: 0; border-radius: 12px; background: linear-gradient(145deg, #2a2a2a, #1f1f1f); display: flex; align-items: center; justify-content: center; font-size: 24px; }
    .cart-item-info { flex: 1; min-width: 0; }
    .cart-item-name { font-size: 14px; font-weight: 700; margin-bottom: 2px; }
    .cart-item-variant { font-size: 11px; color: var(--text-muted); margin-bottom: 4px; }
    .cart-item-price { font-size: 13px; font-weight: 700; color: var(--accent); }
    .cart-item-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
    .cart-qty-btn { width: 28px; height: 28px; border-radius: 8px; background: #2a2a2a; border: 1px solid var(--border); color: white; font-size: 15px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; }
    .cart-qty-val { min-width: 18px; text-align: center; font-weight: 700; font-size: 13px; }
    .cart-remove-btn { width: 28px; height: 28px; border-radius: 8px; background: transparent; border: none; color: var(--text-muted); font-size: 16px; cursor: pointer; }
    .order-type-toggle { display: flex; gap: 8px; margin: 16px 0; }
    .order-type-btn { flex: 1; padding: 12px; text-align: center; background: #2a2a2a; border: 1px solid var(--border); border-radius: 12px; font-size: 13px; font-weight: 700; color: var(--text-muted); cursor: pointer; }
    .order-type-btn.selected { background: var(--primary); border-color: var(--primary); color: white; }
    .field-label { font-size: 13px; font-weight: 700; margin: 14px 0 8px; color: var(--text); }
    .field-input, .field-textarea { width: 100%; background: #2a2a2a; border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px; color: var(--text); font-family: inherit; font-size: 14px; outline: none; resize: none; }
    .field-input:focus, .field-textarea:focus { border-color: var(--primary); }
    .cart-summary-row { display: flex; justify-content: space-between; font-size: 14px; color: var(--text-muted); padding: 4px 0; }
    .cart-summary-row.total { font-size: 18px; font-weight: 800; color: var(--text); padding-top: 10px; margin-top: 6px; border-top: 1px dashed var(--border); }
    .whatsapp-btn { width: 100%; padding: 16px; background: linear-gradient(135deg, #25D366, #128C7E); border: none; border-radius: 14px; color: white; font-family: inherit; font-size: 16px; font-weight: 700; cursor: pointer; margin-top: 18px; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 8px 20px rgba(37, 211, 102, 0.35); }
    .toast { position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%) translateY(20px); background: var(--bg-card-hover); border: 1px solid var(--border); color: var(--text); padding: 12px 20px; border-radius: 12px; font-size: 13px; font-weight: 600; z-index: 400; opacity: 0; pointer-events: none; transition: all 0.25s ease; box-shadow: var(--shadow); }
    .toast.visible { opacity: 1; transform: translateX(-50%) translateY(0); }
    @media (min-width: 600px) { .products-grid { grid-template-columns: 1fr 1fr 1fr; } body { max-width: 680px; margin: 0 auto; border-left: 1px solid #222; border-right: 1px solid #222; } }
  </style>
</head>
<body>

  <header class="header">
    <div class="logo-area">
      <div class="logo-circle">ش</div>
      <div class="brand">
        <div class="brand-name">الشعراوي</div>
        <div class="brand-sub">Sharawy Restaurants</div>
      </div>
    </div>
    <div class="header-actions">
      <button class="icon-btn" title="السلة" onclick="openCart()">🛒</button>
    </div>
  </header>

  <div class="search-bar">
    <div class="search-wrapper">
      <span class="search-icon">🔍</span>
      <input type="text" class="search-input" placeholder="ابحث عن صنف..." id="searchInput" />
    </div>
  </div>

  <div class="categories" id="categories">
    <div class="cat-chip active" data-cat="all">الكل</div>
    <div class="cat-chip" data-cat="offers">عروض الشعراوي</div>
    <div class="cat-chip" data-cat="foul">فول وطعمية</div>
    <div class="cat-chip" data-cat="potato">بطاطس</div>
    <div class="cat-chip" data-cat="meat">لحوم وكريب</div>
    <div class="cat-chip" data-cat="syrian">سوري</div>
    <div class="cat-chip" data-cat="burger">برجر</div>
    <div class="cat-chip" data-cat="boxes">علب وأطباق</div>
    <div class="cat-chip" data-cat="sides">سلطات ومشروبات</div>
  </div>

  <main id="content">
    <section class="section" data-section="offers">
      <div class="section-header"><h2 class="section-title">عروض الشعراوي 🔥</h2></div>
      <div class="products-grid">
        <div class="product-card offer-card" onclick="openModal(this)" data-name="كومبو فول + فلافل + بطاطس" data-price="38" data-desc="1 فول + 1 فلافل + 1 بطاطس صوابع - شامي أو بلدي">
          <div class="product-img combo">🥙</div>
          <div class="product-body">
            <div class="product-name">كومبو فول + فلافل + بطاطس</div>
            <div class="product-desc">1 فول + 1 فلافل + 1 بطاطس صوابع • شامي أو بلدي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 38</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
        <div class="product-card offer-card" onclick="openModal(this)" data-name="كومبو فلافل سوري" data-price="55" data-desc="1 فلافل سوري + 1 بطاطس سوري">
          <div class="product-img combo">🌯</div>
          <div class="product-body">
            <div class="product-name">كومبو فلافل سوري</div>
            <div class="product-desc">1 فلافل سوري + 1 بطاطس سوري</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 55</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" data-section="foul">
      <div class="section-header"><h2 class="section-title">سندوتشات الفول والطعمية</h2></div>
      <div class="products-grid">
        <div class="product-card" onclick="openModal(this)" data-name="فول سادة" data-price="20" data-desc="سندوتش فول سادة • شامي / بلدي">
          <div class="product-img">🫘</div>
          <div class="product-body">
            <div class="product-name">فول سادة</div>
            <div class="product-desc">شامي / بلدي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 20</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
        <div class="product-card" onclick="openModal(this)" data-name="طعمية سادة" data-price="18" data-desc="سندوتش طعمية سادة">
          <div class="product-img">🧆</div>
          <div class="product-body">
            <div class="product-name">طعمية سادة</div>
            <div class="product-desc">شامي / بلدي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 18</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <div class="cart-bar" id="cartBar">
    <button class="cart-btn" onclick="openCart()">
      <div style="display:flex;align-items:center;gap:10px">
        <span class="cart-count" id="cartCount">0</span>
        <span>عرض السلة</span>
      </div>
      <span id="cartTotal">0 ج.م</span>
    </button>
  </div>

  <div class="modal-overlay" id="modal" onclick="closeModal(event)">
    <div class="modal" onclick="event.stopPropagation()">
      <div class="modal-handle"></div>
      <div class="modal-img" id="modalImg">🥙</div>
      <h3 class="modal-title" id="modalTitle">اسم الصنف</h3>
      <div class="modal-price" id="modalPrice">0 ج.م</div>

      <div class="option-group">
        <div class="option-label">اختر الحجم</div>
        <div class="options" id="sizeOptions">
          <div class="option selected" data-extra="0">وسط</div>
          <div class="option" data-extra="10">كبير / فرنساوي</div>
        </div>
      </div>

      <div class="option-group">
        <div class="option-label">نوع الخبز</div>
        <div class="options">
          <div class="option selected">شامي</div>
          <div class="option">بلدي</div>
          <div class="option">فرنساوي</div>
        </div>
      </div>

      <div class="qty-control">
        <button class="qty-btn" onclick="changeQty(-1)">−</button>
        <span class="qty-value" id="qtyValue">1</span>
        <button class="qty-btn" onclick="changeQty(1)">+</button>
      </div>

      <button class="modal-add" onclick="addFromModal()">أضف إلى السلة • <span id="modalTotal">0</span> ج.م</button>
    </div>
  </div>

  <div class="modal-overlay" id="cartModal" onclick="closeCart(event)">
    <div class="modal" onclick="event.stopPropagation()">
      <div class="modal-handle"></div>
      <h3 class="modal-title" style="margin-bottom:16px">سلة الطلبات</h3>

      <div id="cartItemsList"></div>

      <div id="cartCheckoutFields" style="display:none">
        <div class="field-label">نوع الطلب</div>
        <div class="order-type-toggle">
          <div class="order-type-btn selected" data-type="delivery" onclick="setOrderType(this)">🛵 توصيل</div>
          <div class="order-type-btn" data-type="pickup" onclick="setOrderType(this)">🏠 استلام من الفرع</div>
        </div>

        <div class="field-label">الاسم</div>
        <input type="text" class="field-input" id="custName" placeholder="اكتب اسمك" />

        <div class="field-label">رقم الهاتف</div>
        <input type="tel" class="field-input" id="custPhone" placeholder="01xxxxxxxxx" />

        <div class="field-label" id="addressLabel">العنوان</div>
        <textarea class="field-textarea" id="custAddress" rows="2" placeholder="الحي، الشارع، رقم المبنى..."></textarea>

        <div class="field-label">ملاحظات (اختياري)</div>
        <textarea class="field-textarea" id="custNote" rows="2" placeholder="مثال: من غير بصل..."></textarea>

        <div style="margin-top:16px">
          <div class="cart-summary-row total">
            <span>المطلوب دفعه</span>
            <span id="cartSummaryGrandTotal">0 ج.م</span>
          </div>
        </div>

        <button class="whatsapp-btn" onclick="sendOrderViaBackend()">
          <span>🚀</span> تأكيد وإرسال الطلب
        </button>
      </div>
    </div>
  </div>

  <div class="toast" id="toast"></div>

  <script>
    const WHATSAPP_NUMBER = "201055888994";
    let cart = [];
    let currentPrice = 0, currentName = '', currentEmoji = '🍽️', qty = 1, orderType = 'delivery';

    document.querySelectorAll('.cat-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const cat = chip.dataset.cat;
        document.querySelectorAll('.section').forEach(sec => {
          sec.style.display = (cat === 'all' || sec.dataset.section === cat) ? 'block' : 'none';
        });
      });
    });

    document.getElementById('searchInput').addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      document.querySelectorAll('.product-card').forEach(card => {
        const name = card.dataset.name?.toLowerCase() || '';
        card.style.display = (name.includes(q) || !q) ? '' : 'none';
      });
    });

    document.querySelectorAll('.options').forEach(group => {
      group.addEventListener('click', (e) => {
        if (e.target.classList.contains('option')) {
          group.querySelectorAll('.option').forEach(o => o.classList.remove('selected'));
          e.target.classList.add('selected');
          updateModalTotal();
        }
      });
    });

    function openModal(card) {
      currentPrice = parseInt(card.dataset.price) || 0;
      currentName = card.dataset.name;
      currentEmoji = card.querySelector('.product-img')?.textContent || '🍽️';
      qty = 1;

      document.getElementById('qtyValue').textContent = 1;
      document.getElementById('modalTitle').textContent = currentName;
      document.getElementById('modalPrice').textContent = currentPrice + ' ج.م';
      document.getElementById('modalImg').textContent = currentEmoji;
      document.getElementById('modalTotal').textContent = currentPrice;
      document.getElementById('modal').classList.add('open');
    }

    function closeModal(e) { if (e.target.id === 'modal') document.getElementById('modal').classList.remove('open'); }
    function changeQty(delta) { qty = Math.max(1, qty + delta); document.getElementById('qtyValue').textContent = qty; updateModalTotal(); }

    function getModalSelection() {
      let extra = 0; const parts = [];
      document.querySelectorAll('#modal .option-group').forEach(group => {
        const selected = group.querySelector('.option.selected');
        if (selected) {
          parts.push(selected.textContent.trim());
          extra += parseInt(selected.dataset.extra) || 0;
        }
      });
      return { extra, variant: parts.join(' • ') };
    }

    function updateModalTotal() {
      const { extra } = getModalSelection();
      document.getElementById('modalTotal').textContent = (currentPrice + extra) * qty;
    }

    function addFromModal() {
      const { extra, variant } = getModalSelection();
      addItemToCart({ name: currentName, emoji: currentEmoji, unitPrice: currentPrice + extra, variant, qty });
      document.getElementById('modal').classList.remove('open');
      showToast(`تمت إضافة ${currentName} إلى السلة`);
    }

    function quickAdd(btn) {
      const card = btn.closest('.product-card');
      addItemToCart({ name: card.dataset.name, emoji: card.querySelector('.product-img')?.textContent || '🍽️', unitPrice: parseInt(card.dataset.price) || 0, variant: '', qty: 1 });
      showToast(`تمت إضافة ${card.dataset.name} إلى السلة`);
    }

    function addItemToCart(item) {
      const existing = cart.find(it => it.name === item.name && it.variant === item.variant);
      if (existing) existing.qty += item.qty;
      else cart.push({ id: Date.now() + Math.random(), ...item });
      renderCartBadge();
    }

    function getCartTotal() { return cart.reduce((sum, it) => sum + it.unitPrice * it.qty, 0); }
    function getCartCount() { return cart.reduce((sum, it) => sum + it.qty, 0); }

    function renderCartBadge() {
      document.getElementById('cartCount').textContent = getCartCount();
      document.getElementById('cartTotal').textContent = getCartTotal() + ' ج.م';
      document.getElementById('cartBar').classList.toggle('visible', getCartCount() > 0);
    }

    function renderCartItems() {
      const list = document.getElementById('cartItemsList');
      const fields = document.getElementById('cartCheckoutFields');
      if (cart.length === 0) {
        list.innerHTML = `<div class="cart-empty"><div class="cart-empty-icon">🛒</div><div>السلة فاضية دلوقتي</div></div>`;
        fields.style.display = 'none';
        return;
      }
      fields.style.display = 'block';
      list.innerHTML = cart.map(it => `
        <div class="cart-item">
          <div class="cart-item-img">${it.emoji}</div>
          <div class="cart-item-info">
            <div class="cart-item-name">${it.name}</div>
            ${it.variant ? `<div class="cart-item-variant">${it.variant}</div>` : ''}
            <div class="cart-item-price">${it.unitPrice * it.qty} ج.م</div>
          </div>
        </div>
      `).join('');
      document.getElementById('cartSummaryGrandTotal').textContent = getCartTotal() + ' ج.م';
    }

    function openCart() { renderCartItems(); document.getElementById('cartModal').classList.add('open'); }
    function closeCart(e) { if (e.target.id === 'cartModal') document.getElementById('cartModal').classList.remove('open'); }

    function setOrderType(btn) {
      orderType = btn.dataset.type;
      document.querySelectorAll('.order-type-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.classList.add('visible');
      setTimeout(() => toast.classList.remove('visible'), 2200);
    }

    // إرسال الطلب إلى سيرفر بايثون بالخلفية
    async function sendOrderViaBackend() {
      const name = document.getElementById('custName').value.trim();
      const phone = document.getElementById('custPhone').value.trim();
      const address = document.getElementById('custAddress').value.trim();
      const note = document.getElementById('custNote').value.trim();

      if (!name || !phone) { showToast('من فضلك اكتب اسمك ورقم هاتفك'); return; }

      const payload = {
        name, phone, address, note, order_type: orderType,
        items: cart, total: getCartTotal()
      };

      try {
        const response = await fetch('/api/order', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (result.status === 'success') {
          showToast(`تم استلام طلبك بنجاح! رقم الطلب: ${result.order_id}`);
          cart = [];
          renderCartBadge();
          document.getElementById('cartModal').classList.remove('open');
        } else {
          showToast('حدث خطأ أثناء إرسال الطلب');
        }
      } catch (err) {
        showToast('تعذر الاتصال بالسيرفر');
      }
    }
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    # إرجاع ملف الـ HTML وتضمينه مباشرة
    return render_template_string(HTML_MENU)

@app.route('/api/order', methods=['POST'])
def receive_order():
    # إرسال واستقبال الطلبات في السيرفر
    data = request.json
    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({"status": "error", "message": "بيانات غير مكتملة"}), 400
    
    order_id = len(orders_db) + 1
    orders_db.append({
        "id": order_id,
        "customer": data.get('name'),
        "phone": data.get('phone'),
        "address": data.get('address'),
        "type": data.get('order_type'),
        "items": data.get('items', []),
        "total": data.get('total'),
        "note": data.get('note')
    })
    
    return jsonify({"status": "success", "order_id": order_id}), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    # رابط خاص للمطعم لقراءة الطلبات المرسلة: http://your-site/api/orders
    return jsonify({"total_orders": len(orders_db), "orders": orders_db})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
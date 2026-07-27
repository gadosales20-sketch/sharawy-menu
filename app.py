محادثة مع Gemini

تحويل الى ملف بايثون

تم تحويل الكود بالكامل إلى ملف بايثون متكامل باسم sharawy_menu.py.

عند تشغيل هذا الملف باستخدام Python، سيعمل السيرفر تلقائياً ويقوم بإنشاء ملف index.html وفتحه في المتصفح لعرض القائمة الرقمية لمطعم الشعراوي.
رمز PY
sharawy_menu
 PY 


‫Gemini هو نموذج ذكاء اصطناعي وقد ينتج عنه أخطاء.

# -*- coding: utf-8 -*-
"""
سكريبت بايثون لإنشاء وتشغيل المنيو الرقمي لمطعم الشعراوي
Sharawy Digital Menu Web App Generator & Server
"""

import http.server
import socketserver
import os
import webbrowser

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <meta name="description" content="مطعم الشعراوي - قائمة الطعام الرقمية. اطلب فول، طعمية، برجر، بطاطس، سوري وأكثر واستلم طلبك عبر واتساب." />
  <meta name="theme-color" content="#0f0f0f" />
  <meta name="robots" content="index, follow" />
  <meta property="og:title" content="الشعراوي | قائمة الطعام" />
  <meta property="og:description" content="اطلب أشهى السندوتشات والوجبات من مطعم الشعراوي، واستلم تأكيد طلبك مباشرة على واتساب." />
  <meta property="og:type" content="website" />
  <title>الشعراوي | Sharawy Digital Menu</title>
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23e85d04'/%3E%3Ctext x='50' y='68' font-size='55' text-anchor='middle' fill='white' font-family='Arial'%3Eش%3C/text%3E%3C/svg%3E" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #e85d04;       /* برتقالي ناري */
      --primary-dark: #d00000;  /* أحمر غامق */
      --bg-dark: #0f0f0f;
      --bg-card: #1a1a1a;
      --bg-card-hover: #242424;
      --text: #ffffff;
      --text-muted: #b0b0b0;
      --accent: #ffba08;
      --success: #2ecc71;
      --border: #333;
      --radius: 16px;
      --shadow: 0 8px 24px rgba(0,0,0,0.4);
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      font-family: 'Cairo', sans-serif;
      background: var(--bg-dark);
      color: var(--text);
      min-height: 100vh;
      padding-bottom: 90px;
      line-height: 1.5;
    }

    /* ===== Header ===== */
    .header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
      border-bottom: 1px solid var(--border);
      padding: 12px 16px 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .logo-area {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .logo-circle {
      width: 48px;
      height: 48px;
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 18px;
      box-shadow: 0 4px 12px rgba(232, 93, 4, 0.4);
    }

    .brand {
      display: flex;
      flex-direction: column;
    }

    .brand-name {
      font-size: 20px;
      font-weight: 800;
      color: var(--text);
      letter-spacing: -0.5px;
    }

    .brand-sub {
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 400;
    }

    .header-actions {
      display: flex;
      gap: 8px;
    }

    .icon-btn {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text);
      font-size: 18px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .icon-btn:active {
      transform: scale(0.92);
      background: var(--bg-card-hover);
    }

    /* ===== Search ===== */
    .search-bar {
      padding: 0 16px 12px;
      background: #0f0f0f;
    }

    .search-input {
      width: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 12px 16px 12px 44px;
      color: var(--text);
      font-family: inherit;
      font-size: 15px;
      outline: none;
      transition: border-color 0.2s;
    }

    .search-input:focus {
      border-color: var(--primary);
    }

    .search-wrapper {
      position: relative;
    }

    .search-icon {
      position: absolute;
      right: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 18px;
      pointer-events: none;
    }

    /* ===== Categories Scroll ===== */
    .categories {
      display: flex;
      gap: 10px;
      padding: 8px 16px 16px;
      overflow-x: auto;
      scrollbar-width: none;
      -ms-overflow-style: none;
    }

    .categories::-webkit-scrollbar {
      display: none;
    }

    .cat-chip {
      flex-shrink: 0;
      padding: 10px 18px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 50px;
      font-size: 14px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }

    .cat-chip.active {
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      border-color: transparent;
      color: white;
      box-shadow: 0 4px 14px rgba(232, 93, 4, 0.35);
    }

    .cat-chip:active {
      transform: scale(0.96);
    }

    /* ===== Section Title ===== */
    .section {
      padding: 0 16px 24px;
    }

    .section-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
    }

    .section-title {
      font-size: 18px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .section-title::before {
      content: '';
      width: 4px;
      height: 20px;
      background: var(--primary);
      border-radius: 4px;
    }

    /* ===== Product Grid ===== */
    .products-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .product-card {
      background: var(--bg-card);
      border-radius: var(--radius);
      overflow: hidden;
      border: 1px solid var(--border);
      transition: all 0.2s;
      cursor: pointer;
      display: flex;
      flex-direction: column;
    }

    .product-card:active {
      transform: scale(0.98);
      background: var(--bg-card-hover);
    }

    .product-img {
      height: 110px;
      background: linear-gradient(145deg, #2a2a2a, #1f1f1f);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 42px;
      position: relative;
    }

    .product-img.combo {
      background: linear-gradient(145deg, #3d1f00, #1a0f00);
    }

    .badge {
      position: absolute;
      top: 8px;
      right: 8px;
      background: var(--primary);
      color: white;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
    }

    .product-body {
      padding: 12px;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .product-name {
      font-size: 14px;
      font-weight: 700;
      line-height: 1.3;
      color: var(--text);
    }

    .product-desc {
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .product-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: auto;
      padding-top: 8px;
    }

    .price {
      font-size: 16px;
      font-weight: 800;
      color: var(--accent);
    }

    .price span {
      font-size: 11px;
      font-weight: 500;
      color: var(--text-muted);
      margin-right: 2px;
    }

    .add-btn {
      width: 34px;
      height: 34px;
      border-radius: 10px;
      background: var(--primary);
      border: none;
      color: white;
      font-size: 20px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s;
      box-shadow: 0 4px 10px rgba(232, 93, 4, 0.3);
    }

    .add-btn:active {
      transform: scale(0.9);
      background: var(--primary-dark);
    }

    /* ===== Full Width Cards (for offers) ===== */
    .offer-card {
      grid-column: 1 / -1;
      display: flex;
      flex-direction: row;
      height: 120px;
    }

    .offer-card .product-img {
      width: 120px;
      height: 100%;
      flex-shrink: 0;
      font-size: 48px;
    }

    .offer-card .product-body {
      justify-content: center;
    }

    /* ===== Bottom Cart Bar ===== */
    .cart-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(0deg, #1a1a1a 80%, transparent);
      padding: 16px 16px 24px;
      z-index: 200;
      display: none;
    }

    .cart-bar.visible {
      display: block;
    }

    .cart-btn {
      width: 100%;
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      border: none;
      border-radius: 16px;
      padding: 16px 20px;
      color: white;
      font-family: inherit;
      font-size: 16px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 8px 24px rgba(232, 93, 4, 0.4);
      cursor: pointer;
    }

    .cart-count {
      background: white;
      color: var(--primary-dark);
      width: 28px;
      height: 28px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: 800;
    }

    /* ===== Modal (Product Detail) ===== */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.75);
      z-index: 300;
      display: none;
      align-items: flex-end;
      justify-content: center;
    }

    .modal-overlay.open {
      display: flex;
    }

    .modal {
      background: var(--bg-card);
      width: 100%;
      max-width: 480px;
      border-radius: 24px 24px 0 0;
      max-height: 85vh;
      overflow-y: auto;
      padding: 24px 20px 32px;
      animation: slideUp 0.3s ease;
    }

    @keyframes slideUp {
      from { transform: translateY(100%); }
      to { transform: translateY(0); }
    }

    .modal-handle {
      width: 40px;
      height: 4px;
      background: #444;
      border-radius: 4px;
      margin: 0 auto 20px;
    }

    .modal-img {
      height: 160px;
      background: linear-gradient(145deg, #2a2a2a, #1f1f1f);
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 64px;
      margin-bottom: 16px;
    }

    .modal-title {
      font-size: 22px;
      font-weight: 800;
      margin-bottom: 6px;
    }

    .modal-price {
      font-size: 20px;
      font-weight: 800;
      color: var(--accent);
      margin-bottom: 16px;
    }

    .option-group {
      margin-bottom: 18px;
    }

    .option-label {
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 10px;
      color: var(--text);
    }

    .options {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .option {
      padding: 8px 14px;
      background: #2a2a2a;
      border: 1px solid var(--border);
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s;
    }

    .option.selected {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
    }

    .qty-control {
      display: flex;
      align-items: center;
      gap: 16px;
      margin: 20px 0;
    }

    .qty-btn {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: #2a2a2a;
      border: 1px solid var(--border);
      color: white;
      font-size: 20px;
      font-weight: 700;
      cursor: pointer;
    }

    .qty-value {
      font-size: 20px;
      font-weight: 800;
      min-width: 30px;
      text-align: center;
    }

    .modal-add {
      width: 100%;
      padding: 16px;
      background: linear-gradient(135deg, var(--primary), var(--primary-dark));
      border: none;
      border-radius: 14px;
      color: white;
      font-family: inherit;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      margin-top: 8px;
    }

    /* ===== Empty State ===== */
    .empty {
      text-align: center;
      padding: 40px 20px;
      color: var(--text-muted);
    }

    /* ===== Responsive ===== */
    @media (min-width: 600px) {
      .products-grid {
        grid-template-columns: 1fr 1fr 1fr;
      }
      body {
        max-width: 680px;
        margin: 0 auto;
        border-left: 1px solid #222;
        border-right: 1px solid #222;
      }
    }

    /* ===== Cart Modal ===== */
    .cart-empty {
      text-align: center;
      padding: 50px 20px;
      color: var(--text-muted);
    }
    .cart-empty-icon {
      font-size: 48px;
      margin-bottom: 12px;
    }

    .cart-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 0;
      border-bottom: 1px solid var(--border);
    }

    .cart-item:last-of-type {
      border-bottom: none;
    }

    .cart-item-img {
      width: 52px;
      height: 52px;
      flex-shrink: 0;
      border-radius: 12px;
      background: linear-gradient(145deg, #2a2a2a, #1f1f1f);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
    }

    .cart-item-info {
      flex: 1;
      min-width: 0;
    }

    .cart-item-name {
      font-size: 14px;
      font-weight: 700;
      margin-bottom: 2px;
    }

    .cart-item-variant {
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 4px;
    }

    .cart-item-price {
      font-size: 13px;
      font-weight: 700;
      color: var(--accent);
    }

    .cart-item-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }

    .cart-qty-btn {
      width: 28px;
      height: 28px;
      border-radius: 8px;
      background: #2a2a2a;
      border: 1px solid var(--border);
      color: white;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .cart-qty-val {
      min-width: 18px;
      text-align: center;
      font-weight: 700;
      font-size: 13px;
    }

    .cart-remove-btn {
      width: 28px;
      height: 28px;
      border-radius: 8px;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 16px;
      cursor: pointer;
      margin-right: 2px;
    }

    .cart-remove-btn:active {
      color: var(--primary-dark);
    }

    .order-type-toggle {
      display: flex;
      gap: 8px;
      margin: 16px 0;
    }

    .order-type-btn {
      flex: 1;
      padding: 12px;
      text-align: center;
      background: #2a2a2a;
      border: 1px solid var(--border);
      border-radius: 12px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
    }

    .order-type-btn.selected {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
    }

    .field-label {
      font-size: 13px;
      font-weight: 700;
      margin: 14px 0 8px;
      color: var(--text);
    }

    .field-input, .field-textarea {
      width: 100%;
      background: #2a2a2a;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 14px;
      color: var(--text);
      font-family: inherit;
      font-size: 14px;
      outline: none;
      resize: none;
    }

    .field-input:focus, .field-textarea:focus {
      border-color: var(--primary);
    }

    .cart-summary-row {
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      color: var(--text-muted);
      padding: 4px 0;
    }

    .cart-summary-row.total {
      font-size: 18px;
      font-weight: 800;
      color: var(--text);
      padding-top: 10px;
      margin-top: 6px;
      border-top: 1px dashed var(--border);
    }

    .whatsapp-btn {
      width: 100%;
      padding: 16px;
      background: linear-gradient(135deg, #25D366, #128C7E);
      border: none;
      border-radius: 14px;
      color: white;
      font-family: inherit;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      margin-top: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 8px 20px rgba(37, 211, 102, 0.35);
    }

    .whatsapp-btn:active {
      transform: scale(0.98);
    }

    .toast {
      position: fixed;
      bottom: 100px;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      background: var(--bg-card-hover);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 12px 20px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 600;
      z-index: 400;
      opacity: 0;
      pointer-events: none;
      transition: all 0.25s ease;
      box-shadow: var(--shadow);
    }

    .toast.visible {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  </style>
</head>
<body>

  <!-- Header -->
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

  <!-- Search -->
  <div class="search-bar">
    <div class="search-wrapper">
      <span class="search-icon">🔍</span>
      <input type="text" class="search-input" placeholder="ابحث عن صنف..." id="searchInput" />
    </div>
  </div>

  <!-- Categories -->
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

  <!-- Content -->
  <main id="content">

    <!-- Offers -->
    <section class="section" data-section="offers">
      <div class="section-header">
        <h2 class="section-title">عروض الشعراوي 🔥</h2>
      </div>
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

        <div class="product-card offer-card" onclick="openModal(this)" data-name="كومبو فلافل فرنساوي" data-price="60" data-desc="1 فلافل فرنساوي + 1 بطاطس فرنساوي">
          <div class="product-img combo">🥖</div>
          <div class="product-body">
            <div class="product-name">كومبو فلافل فرنساوي</div>
            <div class="product-desc">1 فلافل فرنساوي + 1 بطاطس فرنساوي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 60</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Foul & Taameya -->
    <section class="section" data-section="foul">
      <div class="section-header">
        <h2 class="section-title">سندوتشات الفول والطعمية</h2>
      </div>
      <div class="products-grid">
        <div class="product-card" onclick="openModal(this)" data-name="فول سادة" data-price="20" data-desc="سندوتش فول سادة • شامي / بلدي">
          <div class="product-img">🫘</div>
          <div class="product-body">
            <div class="product-name">فول سادة</div>
            <div class="product-desc">شامي / بلدي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 19-25</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="فول بالزيت" data-price="22" data-desc="فول بزيت الزيتون أو الزيت العادي">
          <div class="product-img">🫒</div>
          <div class="product-body">
            <div class="product-name">فول بالزيت</div>
            <div class="product-desc">زيت زيتون / زيت عادي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 20-27</div>
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
              <div class="price"><span>ج.م</span> 16-20</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="طعمية محشية" data-price="22" data-desc="طعمية محشية بالجبنة أو البيض">
          <div class="product-img">🧀</div>
          <div class="product-body">
            <div class="product-name">طعمية محشية</div>
            <div class="product-desc">جبنة / بيض</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 20-25</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Potato -->
    <section class="section" data-section="potato">
      <div class="section-header">
        <h2 class="section-title">سندوتشات البطاطس</h2>
      </div>
      <div class="products-grid">
        <div class="product-card" onclick="openModal(this)" data-name="بطاطس صوابع" data-price="25" data-desc="بطاطس صوابع مقرمشة">
          <div class="product-img">🍟</div>
          <div class="product-body">
            <div class="product-name">بطاطس صوابع</div>
            <div class="product-desc">شامي / بلدي / فرنساوي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 24-28</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="بطاطس محشية" data-price="28" data-desc="بطاطس محشية باللحمة أو الجبنة">
          <div class="product-img">🥔</div>
          <div class="product-body">
            <div class="product-name">بطاطس محشية</div>
            <div class="product-desc">لحمة / جبنة / بيض</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 26-30</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Meat & Crepe -->
    <section class="section" data-section="meat">
      <div class="section-header">
        <h2 class="section-title">سندوتشات اللحوم والكريب</h2>
      </div>
      <div class="products-grid">
        <div class="product-card" onclick="openModal(this)" data-name="تشيكن بانيه" data-price="95" data-desc="تشيكن بانيه مقرمش">
          <div class="product-img">🍗</div>
          <div class="product-body">
            <div class="product-name">تشيكن بانيه</div>
            <div class="product-desc">وسط / فرنساوي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 85-95</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="زنجر" data-price="100" data-desc="زنجر حار ومقرمش">
          <div class="product-img">🌶️</div>
          <div class="product-body">
            <div class="product-name">زنجر</div>
            <div class="product-desc">وسط / فرنساوي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 90-100</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="شيش طاووق" data-price="100" data-desc="شيش طاووق مشوي">
          <div class="product-img">🍢</div>
          <div class="product-body">
            <div class="product-name">شيش طاووق</div>
            <div class="product-desc">وسط / فرنساوي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 90-100</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="كريب ميكس لحوم" data-price="110" data-desc="كريب ميكس لحوم متنوع">
          <div class="product-img">🌮</div>
          <div class="product-body">
            <div class="product-name">كريب ميكس لحوم</div>
            <div class="product-desc">هوت دوج + برجر + كفتة + سجق</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 110</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Syrian -->
    <section class="section" data-section="syrian">
      <div class="section-header">
        <h2 class="section-title">السوري</h2>
      </div>
      <div class="products-grid">
        <div class="product-card" onclick="openModal(this)" data-name="سوري تشيكن بانيه" data-price="100" data-desc="سوري تشيكن بانيه">
          <div class="product-img">🥙</div>
          <div class="product-body">
            <div class="product-name">سوري تشيكن بانيه</div>
            <div class="product-desc">بانيه شيدر / ميكس</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 100-110</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="سوري كبدة اسكندراني" data-price="80" data-desc="كبدة اسكندراني على الطريقة السورية">
          <div class="product-img">🥩</div>
          <div class="product-body">
            <div class="product-name">سوري كبدة اسكندراني</div>
            <div class="product-desc">كبدة طازجة</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 80</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Burger -->
    <section class="section" data-section="burger">
      <div class="section-header">
        <h2 class="section-title">البرجر</h2>
      </div>
      <div class="products-grid">
        <div class="product-card" onclick="openModal(this)" data-name="بيف برجر كلاسيك" data-price="70" data-desc="برجر لحم كلاسيك">
          <div class="product-img">🍔</div>
          <div class="product-body">
            <div class="product-name">بيف برجر كلاسيك</div>
            <div class="product-desc">لحم بقري طازج</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 70</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="برجر الشعراوي" data-price="110" data-desc="قطعة برجر + زنجر + سلامي + تركي مدخن">
          <div class="product-img">🔥</div>
          <div class="product-body">
            <div class="product-name">برجر الشعراوي</div>
            <div class="product-desc">برجر + زنجر + سلامي + تركي</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 110</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Boxes -->
    <section class="section" data-section="boxes">
      <div class="section-header">
        <h2 class="section-title">العلب والأطباق</h2>
      </div>
      <div class="products-grid">
        <div class="product-card" onclick="openModal(this)" data-name="علبة فول سادة" data-price="28" data-desc="علبة فول سادة • صغير / وسط / كبير">
          <div class="product-img">🥣</div>
          <div class="product-body">
            <div class="product-name">علبة فول سادة</div>
            <div class="product-desc">صغير 10 • وسط 20 • كبير 28</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 10-28</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="أومليت" data-price="30" data-desc="أومليت بالخضار أو الجبنة">
          <div class="product-img">🍳</div>
          <div class="product-body">
            <div class="product-name">أومليت</div>
            <div class="product-desc">خضار / جبنة / بسطرمة</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 25-35</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Sides -->
    <section class="section" data-section="sides">
      <div class="section-header">
        <h2 class="section-title">سلطات ومشروبات</h2>
      </div>
      <div class="products-grid">
        <div class="product-card" onclick="openModal(this)" data-name="سلطة بلدي" data-price="20" data-desc="سلطة بلدي طازجة">
          <div class="product-img">🥗</div>
          <div class="product-body">
            <div class="product-name">سلطة بلدي</div>
            <div class="product-desc">صغير / وسط</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 15-25</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="مياه معدنية" data-price="8" data-desc="مياه معدنية">
          <div class="product-img">💧</div>
          <div class="product-body">
            <div class="product-name">مياه معدنية</div>
            <div class="product-desc">صغيرة / كبيرة</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 8-18</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>

        <div class="product-card" onclick="openModal(this)" data-name="كريب نوتيلا" data-price="65" data-desc="كريب حلو بالنوتيلا">
          <div class="product-img">🍫</div>
          <div class="product-body">
            <div class="product-name">كريب نوتيلا</div>
            <div class="product-desc">كريب حلو</div>
            <div class="product-footer">
              <div class="price"><span>ج.م</span> 65</div>
              <button class="add-btn" onclick="event.stopPropagation(); quickAdd(this)">+</button>
            </div>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- Cart Bar -->
  <div class="cart-bar" id="cartBar">
    <button class="cart-btn" onclick="openCart()">
      <div style="display:flex;align-items:center;gap:10px">
        <span class="cart-count" id="cartCount">0</span>
        <span>عرض السلة</span>
      </div>
      <span id="cartTotal">0 ج.م</span>
    </button>
  </div>

  <!-- Product Modal -->
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
          <div class="option">باتي بان</div>
        </div>
      </div>

      <div class="option-group">
        <div class="option-label">إضافات</div>
        <div class="options">
          <div class="option">بيض +5</div>
          <div class="option">جبنة +8</div>
          <div class="option">بسطرمة +12</div>
          <div class="option">زبدة +3</div>
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

  <!-- Cart / Checkout Modal -->
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
        <textarea class="field-textarea" id="custNote" rows="2" placeholder="مثال: من غير بصل، عايز الأكل سخن..."></textarea>

        <div style="margin-top:16px">
          <div class="cart-summary-row">
            <span>الإجمالي</span>
            <span id="cartSummaryTotal">0 ج.م</span>
          </div>
          <div class="cart-summary-row total">
            <span>المطلوب دفعه</span>
            <span id="cartSummaryGrandTotal">0 ج.م</span>
          </div>
        </div>

        <button class="whatsapp-btn" onclick="sendOrderViaWhatsApp()">
          <span>📲</span> إرسال الطلب عبر واتساب
        </button>
      </div>
    </div>
  </div>

  <div class="toast" id="toast"></div>

  <script>
    // ====== إعدادات المطعم ======
    // ⚠️ غيّر هذا الرقم إلى رقم واتساب المطعم (بصيغة دولية بدون + أو أصفار في البداية)
    // مثال لمصر: كود الدولة 20 ثم الرقم بدون الصفر الأول: 201001234567
    const WHATSAPP_NUMBER = "201055888994";

    let cart = []; // { id, name, emoji, unitPrice, qty, variant }
    let currentPrice = 0;
    let currentName = '';
    let currentEmoji = '🍽️';
    let qty = 1;
    let orderType = 'delivery';

    // Category filter
    document.querySelectorAll('.cat-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const cat = chip.dataset.cat;
        document.querySelectorAll('.section').forEach(sec => {
          if (cat === 'all' || sec.dataset.section === cat) {
            sec.style.display = 'block';
          } else {
            sec.style.display = 'none';
          }
        });
      });
    });

    // Search
    document.getElementById('searchInput').addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      document.querySelectorAll('.product-card').forEach(card => {
        const name = card.dataset.name?.toLowerCase() || '';
        const desc = card.dataset.desc?.toLowerCase() || '';
        card.style.display = (name.includes(q) || desc.includes(q) || !q) ? '' : 'none';
      });
    });

    // Options selection
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
      const name = card.dataset.name;
      const price = parseInt(card.dataset.price) || 0;
      const img = card.querySelector('.product-img')?.textContent || '🍽️';

      currentPrice = price;
      currentName = name;
      currentEmoji = img;
      qty = 1;

      // Reset option selections to the first option in each group
      document.querySelectorAll('#modal .options').forEach(group => {
        group.querySelectorAll('.option').forEach((o, i) => o.classList.toggle('selected', i === 0));
      });

      document.getElementById('qtyValue').textContent = 1;
      document.getElementById('modalTitle').textContent = name;
      document.getElementById('modalPrice').textContent = price + ' ج.م';
      document.getElementById('modalImg').textContent = img;
      document.getElementById('modalTotal').textContent = price;
      document.getElementById('modal').classList.add('open');
    }

    function closeModal(e) {
      if (e.target.id === 'modal') {
        document.getElementById('modal').classList.remove('open');
      }
    }

    function changeQty(delta) {
      qty = Math.max(1, qty + delta);
      document.getElementById('qtyValue').textContent = qty;
      updateModalTotal();
    }

    // يحسب سعر الوحدة الواحدة بعد الإضافات (الحجم + الإضافات)، مع استخراج نص الاختيارات
    function getModalSelection() {
      let extra = 0;
      const parts = [];
      document.querySelectorAll('#modal .option-group').forEach(group => {
        const selected = group.querySelector('.option.selected');
        if (!selected) return;
        const label = group.querySelector('.option-label')?.textContent || '';
        parts.push(selected.textContent.trim());
        // نحاول أخذ القيمة من data-extra، وإن لم توجد نستخرجها من النص مثل "بيض +5"
        let val = selected.dataset.extra;
        if (val === undefined) {
          const m = selected.textContent.match(/\+\s*(\d+)/);
          val = m ? m[1] : 0;
        }
        extra += parseInt(val) || 0;
      });
      return { extra, variant: parts.join(' • ') };
    }

    function updateModalTotal() {
      const { extra } = getModalSelection();
      const total = (currentPrice + extra) * qty;
      document.getElementById('modalTotal').textContent = total;
    }

    function addFromModal() {
      const { extra, variant } = getModalSelection();
      const unitPrice = currentPrice + extra;
      addItemToCart({ name: currentName, emoji: currentEmoji, unitPrice, variant, qty });
      document.getElementById('modal').classList.remove('open');
      showToast(`تمت إضافة ${currentName} إلى السلة`);
    }

    // زر الإضافة السريعة على الكارت (بدون فتح المودال)
    function quickAdd(btn) {
      const card = btn.closest('.product-card');
      const name = card.dataset.name;
      const price = parseInt(card.dataset.price) || 0;
      const emoji = card.querySelector('.product-img')?.textContent || '🍽️';
      addItemToCart({ name, emoji, unitPrice: price, variant: '', qty: 1 });
      showToast(`تمت إضافة ${name} إلى السلة`);
    }

    // الإضافة الفعلية إلى مصفوفة السلة، مع دمج الأصناف المتطابقة (نفس الاسم ونفس الاختيارات)
    function addItemToCart({ name, emoji, unitPrice, variant, qty }) {
      const existing = cart.find(it => it.name === name && it.variant === variant);
      if (existing) {
        existing.qty += qty;
      } else {
        cart.push({ id: Date.now() + Math.random(), name, emoji, unitPrice, variant, qty });
      }
      renderCartBadge();
    }

    function removeCartItem(id) {
      cart = cart.filter(it => it.id !== id);
      renderCartBadge();
      renderCartItems();
    }

    function changeCartItemQty(id, delta) {
      const item = cart.find(it => it.id === id);
      if (!item) return;
      item.qty += delta;
      if (item.qty <= 0) {
        cart = cart.filter(it => it.id !== id);
      }
      renderCartBadge();
      renderCartItems();
    }

    function getCartTotal() {
      return cart.reduce((sum, it) => sum + it.unitPrice * it.qty, 0);
    }

    function getCartCount() {
      return cart.reduce((sum, it) => sum + it.qty, 0);
    }

    function renderCartBadge() {
      const count = getCartCount();
      const total = getCartTotal();
      document.getElementById('cartCount').textContent = count;
      document.getElementById('cartTotal').textContent = total + ' ج.م';
      document.getElementById('cartBar').classList.toggle('visible', count > 0);
    }

    function renderCartItems() {
      const list = document.getElementById('cartItemsList');
      const fields = document.getElementById('cartCheckoutFields');

      if (cart.length === 0) {
        list.innerHTML = `
          <div class="cart-empty">
            <div class="cart-empty-icon">🛒</div>
            <div>السلة فاضية دلوقتي</div>
            <div style="font-size:12px;margin-top:6px">اختار أصنافك المفضلة من القائمة</div>
          </div>`;
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
          <div class="cart-item-actions">
            <button class="cart-remove-btn" onclick="removeCartItem(${JSON.stringify(it.id)})">🗑️</button>
            <button class="cart-qty-btn" onclick="changeCartItemQty(${JSON.stringify(it.id)}, -1)">−</button>
            <span class="cart-qty-val">${it.qty}</span>
            <button class="cart-qty-btn" onclick="changeCartItemQty(${JSON.stringify(it.id)}, 1)">+</button>
          </div>
        </div>
      `).join('');

      const total = getCartTotal();
      document.getElementById('cartSummaryTotal').textContent = total + ' ج.م';
      document.getElementById('cartSummaryGrandTotal').textContent = total + ' ج.م';
    }

    function openCart() {
      renderCartItems();
      document.getElementById('cartModal').classList.add('open');
    }

    function closeCart(e) {
      if (e.target.id === 'cartModal') {
        document.getElementById('cartModal').classList.remove('open');
      }
    }

    function setOrderType(btn) {
      orderType = btn.dataset.type;
      document.querySelectorAll('.order-type-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      const addressLabel = document.getElementById('addressLabel');
      const addressField = document.getElementById('custAddress');
      if (orderType === 'pickup') {
        addressLabel.textContent = 'ملاحظة الاستلام (اختياري)';
        addressField.placeholder = 'مثال: هستلم بعد نص ساعة';
      } else {
        addressLabel.textContent = 'العنوان';
        addressField.placeholder = 'الحي، الشارع، رقم المبنى...';
      }
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.classList.add('visible');
      clearTimeout(window._toastTimer);
      window._toastTimer = setTimeout(() => toast.classList.remove('visible'), 2200);
    }

    function sendOrderViaWhatsApp() {
      if (cart.length === 0) {
        showToast('السلة فاضية، ضيف صنف الأول');
        return;
      }

      const name = document.getElementById('custName').value.trim();
      const phone = document.getElementById('custPhone').value.trim();
      const address = document.getElementById('custAddress').value.trim();
      const note = document.getElementById('custNote').value.trim();

      if (!name || !phone) {
        showToast('من فضلك اكتب اسمك ورقم هاتفك');
        return;
      }
      if (orderType === 'delivery' && !address) {
        showToast('من فضلك اكتب عنوان التوصيل');
        return;
      }

      let msg = `🧾 *طلب جديد - مطعم الشعراوي*\n\n`;
      cart.forEach((it, i) => {
        msg += `${i + 1}. ${it.name} × ${it.qty}\n`;
        if (it.variant) msg += `   (${it.variant})\n`;
        msg += `   ${it.unitPrice * it.qty} ج.م\n`;
      });
      msg += `\n------------------------\n`;
      msg += `*الإجمالي: ${getCartTotal()} ج.م*\n`;
      msg += `نوع الطلب: ${orderType === 'delivery' ? 'توصيل 🛵' : 'استلام من الفرع 🏠'}\n`;
      msg += `الاسم: ${name}\n`;
      msg += `الهاتف: ${phone}\n`;
      if (orderType === 'delivery') msg += `العنوان: ${address}\n`;
      if (note) msg += `ملاحظات: ${note}\n`;

      const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`;
      window.open(url, '_blank');
    }
  </script>
</body>
</html>"""

def generate_html_file(filename="index.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"تم إنشاء ملف HTML بنجاح: {os.path.abspath(filename)}")

def start_server(port=8000):
    generate_html_file()
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"السيرفر يعمل الآن على الرابط: http://localhost:{port}")
        webbrowser.open(f"http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nتم إيقاف السيرفر.")

if __name__ == "__main__":
    start_server()

sharawy_menu.py
جارٍ عرض "sharawy_menu.py".

(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $all(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function say(el, text, isError) {
    if (!el) return;
    el.textContent = text;
    el.classList.toggle("is-error", !!isError);
  }

  /* ---------- Theme toggle (lưu bằng localStorage, có try/catch) ---------- */
  var themeBtn = $("#theme-toggle");
  if (themeBtn) {
    themeBtn.hidden = false;
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  /* ---------- Mobile menu ---------- */
  var menuBtn = $("#menu-btn");
  var nav = $("#site-nav");
  if (menuBtn && nav) {
    menuBtn.hidden = false;
    var setMenu = function (open) {
      nav.classList.toggle("is-open", open);
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.setAttribute("aria-label", menuBtn.getAttribute(open ? "data-label-close" : "data-label-open"));
    };
    menuBtn.addEventListener("click", function () { setMenu(menuBtn.getAttribute("aria-expanded") !== "true"); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menuBtn.getAttribute("aria-expanded") === "true") { setMenu(false); menuBtn.focus(); }
    });
  }

  /* ---------- Highlight mục đang xem ---------- */
  if ("IntersectionObserver" in window) {
    var links = {};
    $all(".nav a[href^='#']").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && links[en.target.id]) {
          $all(".nav a.is-current").forEach(function (a) { a.classList.remove("is-current"); a.removeAttribute("aria-current"); });
          links[en.target.id].classList.add("is-current");
          links[en.target.id].setAttribute("aria-current", "true");
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(links).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
  }

  /* ---------- Copy email / share ---------- */
  var statusEl = $("#action-status");
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) { return navigator.clipboard.writeText(text); }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy") ? resolve() : reject(new Error("copy failed")); }
      catch (e) { reject(e); } finally { document.body.removeChild(ta); }
    });
  }

  var copyBtn = $("#copy-email");
  if (copyBtn) {
    copyBtn.hidden = false;
    copyBtn.addEventListener("click", function () {
      copyText(copyBtn.getAttribute("data-value")).then(
        function () { say(statusEl, copyBtn.getAttribute("data-ok"), false); },
        function () { say(statusEl, copyBtn.getAttribute("data-fail"), true); }
      );
    });
  }

  var shareBtn = $("#share-btn");
  if (shareBtn) {
    shareBtn.hidden = false;
    shareBtn.addEventListener("click", function () {
      var url = window.location.href.split("#")[0];
      var fallback = function () {
        copyText(url).then(
          function () { say(statusEl, shareBtn.getAttribute("data-copied"), false); },
          function () { say(statusEl, shareBtn.getAttribute("data-fail"), true); }
        );
      };
      if (navigator.share) {
        navigator.share({ title: shareBtn.getAttribute("data-title"), url: url }).catch(function (err) {
          if (err && err.name !== "AbortError") fallback();
        });
      } else { fallback(); }
    });
  }

  /* ---------- Lọc + tìm kiếm dự án ---------- */
  var tools = $("#project-tools");
  var items = $all(".project-item");
  if (tools && items.length) {
    tools.hidden = false;
    var search = $("#project-search");
    var empty = $("#project-empty");
    var cat = "all";
    var apply = function () {
      var q = (search.value || "").trim().toLowerCase();
      var shown = 0;
      items.forEach(function (li) {
        var ok = (cat === "all" || li.getAttribute("data-category") === cat) &&
                 (!q || li.getAttribute("data-search").indexOf(q) !== -1);
        li.hidden = !ok;
        if (ok) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
    };
    search.addEventListener("input", apply);
    $all(".filter").forEach(function (btn) {
      btn.addEventListener("click", function () {
        cat = btn.getAttribute("data-filter");
        $all(".filter").forEach(function (b) {
          var on = b === btn;
          b.classList.toggle("is-active", on);
          b.setAttribute("aria-pressed", String(on));
        });
        apply();
      });
    });
  }

  /* ---------- Biểu mẫu liên hệ (chỉ có khi cấu hình endpoint thật) ---------- */
  var form = $("#contact-form");
  if (form) {
    var fstatus = $("#form-status");
    var fields = [
      { el: $("#f-name"), err: $("#f-name-err"), check: function (v) { return v.trim() ? "" : "required"; } },
      { el: $("#f-email"), err: $("#f-email-err"), check: function (v) {
          if (!v.trim()) return "required";
          return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) ? "" : "email"; } },
      { el: $("#f-msg"), err: $("#f-msg-err"), check: function (v) {
          if (!v.trim()) return "required";
          return v.trim().length >= 10 ? "" : "short"; } }
    ];
    var msgFor = function (code) { return form.getAttribute("data-err-" + code); };
    var validate = function () {
      var firstBad = null;
      fields.forEach(function (f) {
        var code = f.check(f.el.value);
        f.err.textContent = code ? msgFor(code) : "";
        f.el.setAttribute("aria-invalid", code ? "true" : "false");
        if (code && !firstBad) firstBad = f.el;
      });
      if (firstBad) firstBad.focus();
      return !firstBad;
    };
    var sending = false;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (sending || !validate()) return;
      if ($("#f-hp").value) return; /* bot: bỏ qua im lặng */
      sending = true;
      var submit = form.querySelector("[type=submit]");
      var label = submit.textContent;
      submit.disabled = true; submit.textContent = form.getAttribute("data-sending");
      say(fstatus, "", false);
      fetch(form.action, {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({ name: $("#f-name").value.trim(), email: $("#f-email").value.trim(), message: $("#f-msg").value.trim() })
      }).then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        form.reset();
        say(fstatus, form.getAttribute("data-success"), false);
      }).catch(function () {
        say(fstatus, form.getAttribute("data-error"), true);
      }).then(function () {
        sending = false; submit.disabled = false; submit.textContent = label;
      });
    });
  }

  /* ---------- Theo dõi click liên kết (kiến trúc sẵn sàng, mặc định không gửi đi đâu) ----------
     Mỗi liên kết có data-track="<id>". Sự kiện "link-click" được phát ra trên document;
     nếu Plausible được bật trong config.py thì gửi thêm custom event. */
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("[data-track]") : null;
    if (!a) return;
    var id = a.getAttribute("data-track");
    try { document.dispatchEvent(new CustomEvent("link-click", { detail: { id: id, href: a.href } })); } catch (err) {}
    if (typeof window.plausible === "function") { window.plausible("Link Click", { props: { id: id } }); }
  });

  /* ---------- Đặt focus vào nội dung khi nhảy anchor (trợ năng) ---------- */
  window.addEventListener("hashchange", function () {
    var t = document.getElementById(location.hash.slice(1));
    if (t) { if (!t.hasAttribute("tabindex")) t.setAttribute("tabindex", "-1"); t.focus({ preventScroll: true }); }
  });
})();

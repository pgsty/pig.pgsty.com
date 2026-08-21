/**
 * PIG landing runtime: command copy, scroll reveal, counter animation.
 * Theme, search, command palette, and menus belong to the OINK shell;
 * nothing here duplicates them.
 */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ============================================
  // Copy buttons
  // ============================================
  function flashCopied(btn) {
    var icon = btn.innerHTML;
    btn.innerHTML = '<span aria-hidden="true">✓</span>';
    btn.classList.add('copied');
    setTimeout(function () {
      btn.innerHTML = icon;
      btn.classList.remove('copied');
    }, 1800);
  }

  function copyText(text, btn) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { flashCopied(btn); }).catch(function () {});
    }
  }

  function initCopyButtons() {
    document.querySelectorAll('[data-copy-text]').forEach(function (btn) {
      btn.addEventListener('click', function () { copyText(btn.dataset.copyText, btn); });
    });

    document.querySelectorAll('.step-cmd-copy').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cmd = btn.closest('.step-cmd');
        var el = cmd && cmd.querySelector('.step-cmd-text');
        if (!el) return;
        copyText(el.dataset.copy || el.textContent, btn);
      });
    });
  }

  // ============================================
  // Scroll reveal
  // ============================================
  function initScrollReveal() {
    var els = document.querySelectorAll('[data-reveal]');
    if (!els.length) return;

    if (!('IntersectionObserver' in window) || reduceMotion) {
      els.forEach(function (el) { el.classList.add('revealed'); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    els.forEach(function (el) { observer.observe(el); });
  }

  // ============================================
  // Counter animation
  // ============================================
  function animateCounter(el, target, duration) {
    duration = duration || 1600;
    var startTime = performance.now();
    function update(now) {
      var p = Math.min((now - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.floor(target * eased).toLocaleString('en-US');
      if (p < 1) requestAnimationFrame(update);
      else el.textContent = target.toLocaleString('en-US');
    }
    requestAnimationFrame(update);
  }

  function initCounters() {
    var els = document.querySelectorAll('[data-count]');
    if (!els.length || reduceMotion || !('IntersectionObserver' in window)) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target, parseInt(entry.target.dataset.count, 10));
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    els.forEach(function (el) { observer.observe(el); });
  }

  // ============================================
  // Init
  // ============================================
  function init() {
    initCopyButtons();
    initScrollReveal();
    initCounters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

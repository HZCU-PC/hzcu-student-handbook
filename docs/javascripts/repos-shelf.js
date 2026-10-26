(function () {
      const main = document.getElementById('repos-main');
      const sideNav = document.getElementById('sideNav');
      const resetCount = document.getElementById('resetCount');
      const recentBlock = document.getElementById('recentBlock');
      const recentToggle = document.getElementById('recentToggle');
      const allBlock = document.getElementById('allBlock');
      const allToggle = document.getElementById('allToggle');
      const searchBox = document.getElementById('searchBox');
      const searchInput = document.getElementById('searchInput');
      const searchClear = document.getElementById('searchClear');
      const searchCount = document.getElementById('searchCount');
      const noResult = document.getElementById('noResult');

      const cats = Array.from(main.querySelectorAll('.cat'));
      const subs = Array.from(main.querySelectorAll('.sub'));
      const catToggles = Array.from(sideNav.querySelectorAll('.cat-toggle'));
      const subItems = Array.from(sideNav.querySelectorAll('.sub-item'));
      const sideGroups = Array.from(sideNav.querySelectorAll('.side-group'));
      const repoItems = Array.from(main.querySelectorAll('.repo-item'));

      // 建立搜索索引：名称 + 描述 + 语言 + 许可证 + 标签
      repoItems.forEach(function (el) {
        el.dataset.search = el.textContent.replace(/\s+/g, ' ').toLowerCase();
      });

      resetCount.textContent = repoItems.length + ' 个仓库';

      // 视图状态：分类筛选 + 搜索词
      const state = { filterType: 'all', filterKey: '', query: '' };

      function clearActive() {
        catToggles.forEach(function (b) { b.classList.remove('active'); });
        subItems.forEach(function (b) { b.classList.remove('active'); });
      }

      function setCollapsed(group, collapsed) {
        group.classList.toggle('collapsed', collapsed);
        const toggle = group.querySelector('.cat-toggle');
        if (toggle) toggle.setAttribute('aria-expanded', String(!collapsed));
      }

      function setRecentCollapsed(collapsed) {
        recentBlock.classList.toggle('collapsed', collapsed);
        recentToggle.setAttribute('aria-expanded', String(!collapsed));
      }

      function setAllCollapsed(collapsed) {
        allBlock.classList.toggle('collapsed', collapsed);
        allToggle.setAttribute('aria-expanded', String(!collapsed));
      }

      function hasFilter() {
        return catToggles.some(function (b) { return b.classList.contains('active'); }) ||
               subItems.some(function (b) { return b.classList.contains('active'); });
      }

      /* 统一渲染：分类筛选 + 搜索词叠加 */
      function applyView() {
        const q = state.query.trim().toLowerCase();

        if (!q) {
          cats.forEach(function (cat) {
            const showCat = state.filterType === 'all' ||
              (state.filterType === 'cat' && cat.dataset.cat === state.filterKey) ||
              (state.filterType === 'sub' && Array.from(cat.querySelectorAll('.sub'))
                .some(function (s) { return s.dataset.sub === state.filterKey; }));
            let visibleSubs = 0;

            Array.from(cat.querySelectorAll('.sub')).forEach(function (sub) {
              const showSub = showCat &&
                (state.filterType !== 'sub' || sub.dataset.sub === state.filterKey);
              const items = Array.from(sub.querySelectorAll('.repo-item'));
              items.forEach(function (it) { it.hidden = false; });
              const empty = sub.querySelector('.repo-empty');
              if (empty) empty.hidden = items.length > 0;
              sub.hidden = !showSub;
              if (showSub) visibleSubs++;
            });

            cat.hidden = !showCat || visibleSubs === 0;
          });

          noResult.hidden = true;
          searchCount.textContent = '';
          return;
        }

        // 搜索模式：忽略分类筛选
        let total = 0;
        cats.forEach(function (cat) {
          let catHits = 0;
          Array.from(cat.querySelectorAll('.sub')).forEach(function (sub) {
            let hits = 0;
            Array.from(sub.querySelectorAll('.repo-item')).forEach(function (it) {
              const ok = it.dataset.search.indexOf(q) !== -1;
              it.hidden = !ok;
              if (ok) hits++;
            });
            const empty = sub.querySelector('.repo-empty');
            if (empty) empty.hidden = true;
            sub.hidden = hits === 0;
            catHits += hits;
          });
          cat.hidden = catHits === 0;
          total += catHits;
        });

        noResult.hidden = total > 0;
        searchCount.textContent = total + ' 个';
      }

      function showAll() {
        clearActive();
        state.filterType = 'all';
        state.filterKey = '';
        applyView();
        main.scrollTop = 0;
      }

      function showCat(catKey) {
        clearActive();
        const btn = catToggles.find(function (b) { return b.dataset.cat === catKey; });
        if (btn) btn.classList.add('active');
        setRecentCollapsed(true);
        setAllCollapsed(false);
        state.filterType = 'cat';
        state.filterKey = catKey;
        applyView();
        main.scrollTop = 0;
      }

      function showSub(subKey) {
        clearActive();
        const btn = subItems.find(function (b) { return b.dataset.sub === subKey; });
        if (btn) btn.classList.add('active');
        setRecentCollapsed(true);
        setAllCollapsed(false);
        state.filterType = 'sub';
        state.filterKey = subKey;
        applyView();
        main.scrollTop = 0;
      }

      /* ---------- 搜索 ---------- */
      function syncSearchUI() {
        searchBox.classList.toggle('has-value', searchInput.value.length > 0);
      }

      searchInput.addEventListener('input', function () {
        state.query = searchInput.value;
        syncSearchUI();
        if (state.query.trim()) clearActive();
        applyView();
      });

      searchClear.addEventListener('click', function () {
        searchInput.value = '';
        state.query = '';
        syncSearchUI();
        applyView();
        searchInput.focus();
      });

      searchInput.addEventListener('keydown', function (ev) {
        if (ev.key === 'Escape') { ev.preventDefault(); searchClear.click(); }
      });

      // 按 "/" 快速聚焦搜索框
      document.addEventListener('keydown', function (ev) {
        if (ev.key === '/' && document.activeElement !== searchInput) {
          ev.preventDefault();
          searchInput.focus();
        }
      });

      /* ---------- 侧栏交互 ---------- */
      recentToggle.addEventListener('click', function () {
        setRecentCollapsed(!recentBlock.classList.contains('collapsed'));
      });

      allToggle.addEventListener('click', function () {
        const collapsed = allBlock.classList.contains('collapsed');
        if (hasFilter()) {
          setAllCollapsed(false);
          showAll();
          return;
        }
        setAllCollapsed(!collapsed);
      });

      catToggles.forEach(function (btn) {
        btn.addEventListener('click', function () {
          const key = btn.dataset.cat;
          const group = btn.closest('.side-group');
          const isActive = btn.classList.contains('active');
          const isCollapsed = group.classList.contains('collapsed');

          if (isCollapsed) {
            setCollapsed(group, false);
            if (!isActive) showCat(key);
            return;
          }

          if (!isActive) {
            showCat(key);
            setCollapsed(group, false);
            sideGroups.forEach(function (g) {
              if (g !== group) setCollapsed(g, true);
            });
            return;
          }

          setCollapsed(group, true);
        });
      });

      subItems.forEach(function (btn) {
        btn.addEventListener('click', function () {
          const key = btn.dataset.sub;
          if (btn.classList.contains('active')) {
            showAll();
            return;
          }
          showSub(key);
        });
      });

      /* ---------- 最近收录跳转 ---------- */
      document.querySelectorAll('[data-jump]').forEach(function (link) {
        link.addEventListener('click', function (ev) {
          ev.preventDefault();
          const id = link.getAttribute('href').slice(1);
          const target = document.getElementById(id);
          if (!target) return;

          searchInput.value = '';
          state.query = '';
          syncSearchUI();
          showAll();

          requestAnimationFrame(function () {
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            target.classList.add('flash');
            setTimeout(function () { target.classList.remove('flash'); }, 1600);
          });
        });
      });

      // 初始状态：只展开「最近收录」和「全部」，6 个大类默认收起
      sideGroups.forEach(function (g) { setCollapsed(g, true); });
      applyView();
    })();
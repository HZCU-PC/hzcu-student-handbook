# 优质 GitHub 仓库介绍

> 规矩立得住，才能不烧心：精选解决真实问题、文档能让人快速跑通、代码规范且持续维护的开源仓库——看得懂、跑得起来、敢放心依赖。

<div class="repos-page">
  <div class="repos-search">
    <div class="search-box" id="searchBox">
            <span class="search-icon" aria-hidden="true">⌕</span>
            <input id="searchInput" type="search" placeholder="搜索仓库…" autocomplete="off" spellcheck="false" aria-label="搜索仓库">
            <span class="search-count" id="searchCount"></span>
            <button type="button" id="searchClear" aria-label="清空搜索">✕</button>
          </div>
  </div>
<div class="app">

    <aside class="region region-sidebar">


      <nav class="side-nav" id="sideNav" aria-label="仓库分类">
        <!-- 顶层 1：最近收录 -->
        <div class="side-block" id="recentBlock">
          <button type="button" class="side-head" id="recentToggle" aria-expanded="true" aria-controls="recentBody">
            <span class="head-title">最近收录</span>
            <span class="caret">▾</span>
          </button>
          <div class="block-body" id="recentBody">
            <ul class="recent-list">
              <li><a class="recent-item" href="#r-krahets-hello-algo" data-jump>krahets/hello-algo</a></li>
              <li><a class="recent-item" href="#r-duckdb-duckdb" data-jump>duckdb/duckdb</a></li>
              <li><a class="recent-item" href="#r-langgenius-dify" data-jump>langgenius/dify</a></li>
              <li><a class="recent-item" href="#r-ollama-ollama" data-jump>ollama/ollama</a></li>
              <li><a class="recent-item" href="#r-microsoft-vscode" data-jump>microsoft/vscode</a></li>
            </ul>
          </div>
        </div>

        <!-- 顶层 2：全部（罗马数字分类是它的子目录） -->
        <div class="side-block" id="allBlock">
          <button type="button" class="side-head" id="allToggle" aria-expanded="true" aria-controls="allBody">
            <span class="head-title">全部</span>
            <span class="reset-count" id="resetCount">59 个仓库</span>
            <span class="caret">▾</span>
          </button>
          <div class="block-body all-body" id="allBody">
        <!-- Ⅰ 打基础 -->
        <div class="side-group" data-cat="foundation">
          <button type="button" class="cat-toggle" data-cat="foundation" aria-expanded="true">
            <span class="cat-num">Ⅰ</span>
            <span class="cat-name">打基础</span>
            <span class="caret">▾</span>
          </button>
          <ul class="sub-list">
            <li><button type="button" class="sub-item" data-sub="algo">算法与数据结构<span class="sub-n">4</span></button></li>
            <li><button type="button" class="sub-item" data-sub="system">计算机系统<span class="sub-n">3</span></button></li>
            <li><button type="button" class="sub-item" data-sub="lang">语言深入<span class="sub-n">6</span></button></li>
          </ul>
        </div>

        <!-- Ⅱ 动手造 -->
        <div class="side-group" data-cat="build">
          <button type="button" class="cat-toggle" data-cat="build" aria-expanded="true">
            <span class="cat-num">Ⅱ</span>
            <span class="cat-name">动手造</span>
            <span class="caret">▾</span>
          </button>
          <ul class="sub-list">
            <li><button type="button" class="sub-item" data-sub="wheels">从零造轮子<span class="sub-n">1</span></button></li>
            <li><button type="button" class="sub-item" data-sub="web">Web 全栈<span class="sub-n">5</span></button></li>
            <li><button type="button" class="sub-item" data-sub="data">数据与后端<span class="sub-n">2</span></button></li>
          </ul>
        </div>

        <!-- Ⅲ 用 AI -->
        <div class="side-group" data-cat="ai">
          <button type="button" class="cat-toggle" data-cat="ai" aria-expanded="true">
            <span class="cat-num">Ⅲ</span>
            <span class="cat-name">用 AI</span>
            <span class="caret">▾</span>
          </button>
          <ul class="sub-list">
            <li><button type="button" class="sub-item" data-sub="agent">Agent 与编排<span class="sub-n">6</span></button></li>
            <li><button type="button" class="sub-item" data-sub="infer">本地推理<span class="sub-n">6</span></button></li>
            <li><button type="button" class="sub-item" data-sub="rag">RAG、记忆与评测<span class="sub-n">6</span></button></li>
          </ul>
        </div>

        <!-- Ⅳ 提效率 -->
        <div class="side-group" data-cat="tools">
          <button type="button" class="cat-toggle" data-cat="tools" aria-expanded="true">
            <span class="cat-num">Ⅳ</span>
            <span class="cat-name">提效率</span>
            <span class="caret">▾</span>
          </button>
          <ul class="sub-list">
            <li><button type="button" class="sub-item" data-sub="editor">编辑器与终端<span class="sub-n">2</span></button></li>
            <li><button type="button" class="sub-item" data-sub="devkit">开发工具链<span class="sub-n">3</span></button></li>
            <li><button type="button" class="sub-item" data-sub="desktop">桌面效率<span class="sub-n">5</span></button></li>
          </ul>
        </div>

        <!-- Ⅴ 上线跑 -->
        <div class="side-group" data-cat="ship">
          <button type="button" class="cat-toggle" data-cat="ship" aria-expanded="true">
            <span class="cat-num">Ⅴ</span>
            <span class="cat-name">上线跑</span>
            <span class="caret">▾</span>
          </button>
          <ul class="sub-list">
            <li><button type="button" class="sub-item" data-sub="ops">容器与运维<span class="sub-n">1</span></button></li>
            <li><button type="button" class="sub-item" data-sub="selfhost">自托管与媒体<span class="sub-n">4</span></button></li>
          </ul>
        </div>

        <!-- Ⅵ 长本事 -->
        <div class="side-group" data-cat="grow">
          <button type="button" class="cat-toggle" data-cat="grow" aria-expanded="true">
            <span class="cat-num">Ⅵ</span>
            <span class="cat-name">长本事</span>
            <span class="caret">▾</span>
          </button>
          <ul class="sub-list">
            <li><button type="button" class="sub-item" data-sub="interview">面试与系统设计<span class="sub-n">2</span></button></li>
            <li><button type="button" class="sub-item" data-sub="roadmap">学习路线与资源<span class="sub-n">3</span></button></li>
          </ul>
        </div>
          </div>
        </div>
      </nav>
    </aside>

    <main class="region region-main" id="repos-main">
      <div class="no-result" id="noResult" hidden>没有匹配的仓库，换个关键词试试。</div>

      <!-- ========== Ⅰ 打基础 ========== -->
      <section class="cat" data-cat="foundation">
        <h2 class="cat-head"><span class="cat-num">Ⅰ</span>打基础</h2>
        <p class="cat-note">地基不牢，后面全是补丁。算法、系统、语言这三样，决定你能走多远。</p>

        <section class="sub" data-sub="algo">
          <h3 class="sub-head">算法与数据结构<span class="sub-count">4</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-krahets-hello-algo">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">K</span><img class="avatar-img" src="https://github.com/krahets.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/krahets/hello-algo" target="_blank" rel="noopener">krahets/hello-algo</a>
                  <span class="repo-stars">★ 131.1k</span>
                </div>
                <p class="repo-desc">动画图解数据结构与算法，多语言代码。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#b07219"></i>Java</span><span class="meta-item">⑂ 15.5k</span><a class="meta-home" href="https://www.hello-algo.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>algo</li><li>algorithm</li><li>algorithms</li><li>book</li><li>data-structure</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-labuladong-fucking-algorithm">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">L</span><img class="avatar-img" src="https://github.com/labuladong.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/labuladong/fucking-algorithm" target="_blank" rel="noopener">labuladong/fucking-algorithm</a>
                  <span class="repo-stars">★ 136k</span>
                </div>
                <p class="repo-desc">算法套路模板，把刷题框架讲清楚，中文。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#083fa1"></i>Markdown</span><span class="meta-item">⑂ 23.5k</span><a class="meta-home" href="https://labuladong.online/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>algorithms</li><li>computer-science</li><li>data-structures</li><li>dynamic-programming</li><li>interview-questions</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-youngyangyang04-leetcode-master">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">Y</span><img class="avatar-img" src="https://github.com/youngyangyang04.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/youngyangyang04/leetcode-master" target="_blank" rel="noopener">youngyangyang04/leetcode-master</a>
                  <span class="repo-stars">★ 62.7k</span>
                </div>
                <p class="repo-desc">代码随想录：题解 + 刷题顺序，常见题型全覆盖。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#89e051"></i>Shell</span><span class="meta-item">⑂ 12.3k</span></div>
                <ul class="repo-topics"><li>algorithm</li><li>cpp</li><li>go</li><li>interview</li><li>java</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-thealgorithms-python">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">T</span><img class="avatar-img" src="https://github.com/TheAlgorithms.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/TheAlgorithms/Python" target="_blank" rel="noopener">TheAlgorithms/Python</a>
                  <span class="repo-stars">★ 225.5k</span>
                </div>
                <p class="repo-desc">用 Python 实现常见算法与数据结构，适合对照源码学习。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 51.2k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://thealgorithms.github.io/Python/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>algorithm</li><li>algorithm-competitions</li><li>algorithms-implemented</li><li>algos</li><li>community-driven</li></ul>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="system">
          <h3 class="sub-head">计算机系统<span class="sub-count">3</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-mit-pdos-xv6-riscv">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">M</span><img class="avatar-img" src="https://github.com/mit-pdos.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/mit-pdos/xv6-riscv" target="_blank" rel="noopener">mit-pdos/xv6-riscv</a>
                  <span class="repo-stars">★ 10.7k</span>
                </div>
                <p class="repo-desc">MIT 操作系统课内核，动手改系统调用、页表、锁和文件系统。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#555555"></i>C</span><span class="meta-item">⑂ 4.5k</span><a class="meta-home" href="https://pdos.csail.mit.edu/6.1810" target="_blank" rel="noopener">官网</a></div>
              </div>
            </li>
            <li class="repo-item" id="r-cmu-db-bustub">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">C</span><img class="avatar-img" src="https://github.com/cmu-db.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/cmu-db/bustub" target="_blank" rel="noopener">cmu-db/bustub</a>
                  <span class="repo-stars">★ 5.1k</span>
                </div>
                <p class="repo-desc">CMU 数据库内核实验：Buffer Pool、B+ 树、查询执行与并发控制。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#f34b7d"></i>C++</span><span class="meta-item">⑂ 2.1k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://15445.courses.cs.cmu.edu" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>database</li><li>dbms</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-cfenollosa-os-tutorial">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">C</span><img class="avatar-img" src="https://github.com/cfenollosa.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/cfenollosa/os-tutorial" target="_blank" rel="noopener">cfenollosa/os-tutorial</a>
                  <span class="repo-stars">★ 30.8k</span>
                </div>
                <p class="repo-desc">从 bootloader 写到用户态，一章一个可运行目标。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#555555"></i>C</span><span class="meta-item">⑂ 3.6k</span><span class="meta-item">BSD 3-Clause</span></div>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="lang">
          <h3 class="sub-head">语言深入<span class="sub-count">6</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-rust-lang-rustlings">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">R</span><img class="avatar-img" src="https://github.com/rust-lang.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/rust-lang/rustlings" target="_blank" rel="noopener">rust-lang/rustlings</a>
                  <span class="repo-stars">★ 64.5k</span>
                </div>
                <p class="repo-desc">80+ 道小练习，改到编译通过为止。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#dea584"></i>Rust</span><span class="meta-item">⑂ 11.3k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://rustlings.rust-lang.org" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>beginner-friendly</li><li>exercises</li><li>rust</li><li>rustlings</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-type-challenges-type-challenges">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">T</span><img class="avatar-img" src="https://github.com/type-challenges.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/type-challenges/type-challenges" target="_blank" rel="noopener">type-challenges/type-challenges</a>
                  <span class="repo-stars">★ 48.5k</span>
                </div>
                <p class="repo-desc">TypeScript 类型体操，从 easy 刷到 extreme。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 5.3k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://tsch.js.org/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>challenges</li><li>type</li><li>type-system</li><li>typescript</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-exercism-exercism">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">E</span><img class="avatar-img" src="https://github.com/exercism.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/exercism/exercism" target="_blank" rel="noopener">exercism/exercism</a>
                  <span class="repo-stars">★ 7.6k</span>
                </div>
                <p class="repo-desc">70+ 语言练习题库 + CLI，做完提交可看社区解法。</p>
                <div class="repo-meta"><span class="meta-item">⑂ 1k</span><a class="meta-home" href="https://exercism.org" target="_blank" rel="noopener">官网</a></div>
              </div>
            </li>
            <li class="repo-item" id="r-rust-lang-book">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">R</span><img class="avatar-img" src="https://github.com/rust-lang.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/rust-lang/book" target="_blank" rel="noopener">rust-lang/book</a>
                  <span class="repo-stars">★ 18.5k</span>
                </div>
                <p class="repo-desc">官方 Rust 教材，从所有权讲到并发，配套在线书站。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#dea584"></i>Rust</span><span class="meta-item">⑂ 4.2k</span><a class="meta-home" href="https://doc.rust-lang.org/book/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>book</li><li>mdbook</li><li>rust</li><li>rust-programming-language</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-jackfrued-python-100-days">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">J</span><img class="avatar-img" src="https://github.com/jackfrued.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/jackfrued/Python-100-Days" target="_blank" rel="noopener">jackfrued/Python-100-Days</a>
                  <span class="repo-stars">★ 187.4k</span>
                </div>
                <p class="repo-desc">100 天 Python 实践计划，爬虫、Django、数据分析都有项目。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#DA5B0B"></i>Jupyter Notebook</span><span class="meta-item">⑂ 55.7k</span></div>
              </div>
            </li>
            <li class="repo-item" id="r-getify-you-dont-know-js">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">G</span><img class="avatar-img" src="https://github.com/getify.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/getify/You-Dont-Know-JS" target="_blank" rel="noopener">getify/You-Dont-Know-JS</a>
                  <span class="repo-stars">★ 184.8k</span>
                </div>
                <p class="repo-desc">JS 作用域、闭包、原型与异步逐本讲透。</p>
                <div class="repo-meta"><span class="meta-item">⑂ 33.3k</span></div>
                <ul class="repo-topics"><li>async</li><li>book</li><li>book-series</li><li>closures</li><li>education</li></ul>
              </div>
            </li>
          </ul>
        </section>
      </section>

      <!-- ========== Ⅱ 动手造 ========== -->
      <section class="cat" data-cat="build">
        <h2 class="cat-head"><span class="cat-num">Ⅱ</span>动手造</h2>
        <p class="cat-note">看懂不等于会写。把东西从零造一遍，才知道每一层在解决什么问题。</p>

        <section class="sub" data-sub="wheels">
          <h3 class="sub-head">从零造轮子<span class="sub-count">1</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-codecrafters-io-build-your-own-x">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">C</span><img class="avatar-img" src="https://github.com/codecrafters-io.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/codecrafters-io/build-your-own-x" target="_blank" rel="noopener">codecrafters-io/build-your-own-x</a>
                  <span class="repo-stars">★ 556.1k</span>
                </div>
                <p class="repo-desc">用任意语言重造 Redis、Git、Docker 等项目。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#083fa1"></i>Markdown</span><span class="meta-item">⑂ 52.1k</span><a class="meta-home" href="https://codecrafters.io" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>awesome-list</li><li>free</li><li>programming</li><li>tutorial-code</li><li>tutorial-exercises</li></ul>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="web">
          <h3 class="sub-head">Web 全栈<span class="sub-count">5</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-react-react">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">R</span><img class="avatar-img" src="https://github.com/react.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/react/react" target="_blank" rel="noopener">react/react</a>
                  <span class="repo-stars">★ 251.8k</span>
                </div>
                <p class="repo-desc">声明式 UI 库，前端最主流的框架。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#f1e05a"></i>JavaScript</span><span class="meta-item">⑂ 51.6k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://react.dev" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>declarative</li><li>frontend</li><li>javascript</li><li>library</li><li>react</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-vercel-next-js">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">V</span><img class="avatar-img" src="https://github.com/vercel.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/vercel/next.js" target="_blank" rel="noopener">vercel/next.js</a>
                  <span class="repo-stars">★ 143.2k</span>
                </div>
                <p class="repo-desc">React 全栈框架，支持 App Router、SSR 与 Server Actions。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#f1e05a"></i>JavaScript</span><span class="meta-item">⑂ 34.5k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://nextjs.org" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>blog</li><li>browser</li><li>compiler</li><li>components</li><li>hybrid</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-shadcn-ui-ui">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">S</span><img class="avatar-img" src="https://github.com/shadcn-ui.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/shadcn-ui/ui" target="_blank" rel="noopener">shadcn-ui/ui</a>
                  <span class="repo-stars">★ 126.5k</span>
                </div>
                <p class="repo-desc">可直接复制进项目的 Tailwind 组件库。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 13k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://ui.shadcn.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>base-ui</li><li>components</li><li>gen-ui</li><li>generative-ai</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-supabase-supabase">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">S</span><img class="avatar-img" src="https://github.com/supabase.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/supabase/supabase" target="_blank" rel="noopener">supabase/supabase</a>
                  <span class="repo-stars">★ 113.9k</span>
                </div>
                <p class="repo-desc">Postgres + Auth + Storage + Realtime + Edge Functions。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 16.7k</span><span class="meta-item">Apache License 2.0</span><a class="meta-home" href="https://supabase.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>alternative</li><li>auth</li><li>database</li><li>deno</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-pocketbase-pocketbase">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">P</span><img class="avatar-img" src="https://github.com/pocketbase.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/pocketbase/pocketbase" target="_blank" rel="noopener">pocketbase/pocketbase</a>
                  <span class="repo-stars">★ 61.6k</span>
                </div>
                <p class="repo-desc">单文件后端：SQLite + Auth + Realtime + 管理后台。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#00ADD8"></i>Go</span><span class="meta-item">⑂ 3.7k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://pocketbase.io" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>authentication</li><li>backend</li><li>golang</li><li>realtime</li></ul>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="data">
          <h3 class="sub-head">数据与后端<span class="sub-count">2</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-duckdb-duckdb">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">D</span><img class="avatar-img" src="https://github.com/duckdb.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/duckdb/duckdb" target="_blank" rel="noopener">duckdb/duckdb</a>
                  <span class="repo-stars">★ 42.5k</span>
                </div>
                <p class="repo-desc">嵌入式 OLAP 数据库，一条 SQL 直接查 Parquet/CSV。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#f34b7d"></i>C++</span><span class="meta-item">⑂ 4k</span><span class="meta-item">MIT License</span><a class="meta-home" href="http://www.duckdb.org" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>analytics</li><li>database</li><li>embedded-database</li><li>olap</li><li>sql</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-pola-rs-polars">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">P</span><img class="avatar-img" src="https://github.com/pola-rs.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/pola-rs/polars" target="_blank" rel="noopener">pola-rs/polars</a>
                  <span class="repo-stars">★ 40.2k</span>
                </div>
                <p class="repo-desc">Rust 实现的 DataFrame，惰性执行、多线程。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#dea584"></i>Rust</span><span class="meta-item">⑂ 3.2k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://docs.pola.rs" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>arrow</li><li>dataframe</li><li>dataframe-library</li><li>dataframes</li><li>out-of-core</li></ul>
              </div>
            </li>
          </ul>
        </section>
      </section>

      <!-- ========== Ⅲ 用 AI ========== -->
      <section class="cat" data-cat="ai">
        <h2 class="cat-head"><span class="cat-num">Ⅲ</span>用 AI</h2>
        <p class="cat-note">这一代开发者绕不开的能力：会调、会跑、会评估，而不是只会聊天。</p>

        <section class="sub" data-sub="agent">
          <h3 class="sub-head">Agent 与编排<span class="sub-count">6</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-openclaw-openclaw">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">O</span><img class="avatar-img" src="https://github.com/openclaw.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/openclaw/openclaw" target="_blank" rel="noopener">openclaw/openclaw</a>
                  <span class="repo-stars">★ 393k</span>
                </div>
                <p class="repo-desc">本地个人 AI 助手，网关接入 20+ 聊天平台，提供多端客户端。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 82.6k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://openclaw.ai" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>assistant</li><li>crustacean</li><li>molty</li><li>openclaw</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-nousresearch-hermes-agent">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">N</span><img class="avatar-img" src="https://github.com/NousResearch.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/NousResearch/hermes-agent" target="_blank" rel="noopener">NousResearch/hermes-agent</a>
                  <span class="repo-stars">★ 256.9k</span>
                </div>
                <p class="repo-desc">通用 AI Agent，模型可自由切换，内置定时任务与多种沙盒。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 56.2k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://hermes-agent.nousresearch.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>ai-agent</li><li>ai-agents</li><li>anthropic</li><li>chatgpt</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-langgenius-dify">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">L</span><img class="avatar-img" src="https://github.com/langgenius.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/langgenius/dify" target="_blank" rel="noopener">langgenius/dify</a>
                  <span class="repo-stars">★ 159.5k</span>
                </div>
                <p class="repo-desc">低代码 LLM 应用开发平台，可视化编排工作流、RAG 与 Agent。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 25.2k</span><a class="meta-home" href="https://dify.ai" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>agent</li><li>agentic-ai</li><li>agentic-framework</li><li>agentic-workflow</li><li>ai</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-langchain-ai-langgraph">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">L</span><img class="avatar-img" src="https://github.com/langchain-ai.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/langchain-ai/langgraph" target="_blank" rel="noopener">langchain-ai/langgraph</a>
                  <span class="repo-stars">★ 43.9k</span>
                </div>
                <p class="repo-desc">图/状态机编排有状态 Agent，适合复杂分支与人工审核。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 7.5k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://docs.langchain.com/oss/python/langgraph/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>agents</li><li>ai</li><li>ai-agents</li><li>chatgpt</li><li>deepagents</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-openai-openai-agents-python">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">O</span><img class="avatar-img" src="https://github.com/openai.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/openai/openai-agents-python" target="_blank" rel="noopener">openai/openai-agents-python</a>
                  <span class="repo-stars">★ 30.3k</span>
                </div>
                <p class="repo-desc">轻量 Agent 框架，内置 handoff、guardrails 与 tracing。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 4.9k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://openai.github.io/openai-agents-python/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>agents</li><li>ai</li><li>framework</li><li>harness</li><li>llm</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-modelcontextprotocol-servers">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">M</span><img class="avatar-img" src="https://github.com/modelcontextprotocol.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/modelcontextprotocol/servers" target="_blank" rel="noopener">modelcontextprotocol/servers</a>
                  <span class="repo-stars">★ 91.5k</span>
                </div>
                <p class="repo-desc">MCP 官方参考服务器，让模型连接文件、Git、数据库等工具。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 11.9k</span><a class="meta-home" href="https://modelcontextprotocol.io" target="_blank" rel="noopener">官网</a></div>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="infer">
          <h3 class="sub-head">本地推理<span class="sub-count">6</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-open-webui-open-webui">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">O</span><img class="avatar-img" src="https://github.com/open-webui.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/open-webui/open-webui" target="_blank" rel="noopener">open-webui/open-webui</a>
                  <span class="repo-stars">★ 156.7k</span>
                </div>
                <p class="repo-desc">自托管 ChatGPT 式界面，接入 Ollama 或任意 OpenAI 兼容 API。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 22.8k</span><a class="meta-home" href="https://openwebui.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>llm</li><li>llm-ui</li><li>llm-webui</li><li>llms</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-comfy-org-comfyui">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">C</span><img class="avatar-img" src="https://github.com/Comfy-Org.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/Comfy-Org/ComfyUI" target="_blank" rel="noopener">Comfy-Org/ComfyUI</a>
                  <span class="repo-stars">★ 142.8k</span>
                </div>
                <p class="repo-desc">节点式扩散模型推理界面，本地运行 SD、Flux 等模型。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 16.8k</span><span class="meta-item">GNU General Public License v3.0</span><a class="meta-home" href="https://www.comfy.org/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>comfy</li><li>comfyui</li><li>python</li><li>pytorch</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-ollama-ollama">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">O</span><img class="avatar-img" src="https://github.com/ollama.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/ollama/ollama" target="_blank" rel="noopener">ollama/ollama</a>
                  <span class="repo-stars">★ 184.7k</span>
                </div>
                <p class="repo-desc">一条命令在本地跑开源模型，提供 OpenAI 兼容 API。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#00ADD8"></i>Go</span><span class="meta-item">⑂ 18.6k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://ollama.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>deepseek</li><li>gemma</li><li>gemma3</li><li>glm</li><li>go</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-vllm-project-vllm">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">V</span><img class="avatar-img" src="https://github.com/vllm-project.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/vllm-project/vllm" target="_blank" rel="noopener">vllm-project/vllm</a>
                  <span class="repo-stars">★ 95.4k</span>
                </div>
                <p class="repo-desc">高吞吐推理服务，支持 PagedAttention 与连续批处理。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 23.9k</span><span class="meta-item">Apache License 2.0</span><a class="meta-home" href="https://vllm.ai" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>amd</li><li>blackwell</li><li>cuda</li><li>deepseek</li><li>deepseek-v3</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-sgl-project-sglang">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">S</span><img class="avatar-img" src="https://github.com/sgl-project.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/sgl-project/sglang" target="_blank" rel="noopener">sgl-project/sglang</a>
                  <span class="repo-stars">★ 38.1k</span>
                </div>
                <p class="repo-desc">高性能 Serving 框架，适合高并发与结构化生成。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 9.9k</span><span class="meta-item">Apache License 2.0</span><a class="meta-home" href="https://sglang.io" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>attention</li><li>blackwell</li><li>cuda</li><li>deepseek</li><li>diffusion</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-huggingface-transformers">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">H</span><img class="avatar-img" src="https://github.com/huggingface.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/huggingface/transformers" target="_blank" rel="noopener">huggingface/transformers</a>
                  <span class="repo-stars">★ 168.1k</span>
                </div>
                <p class="repo-desc">模型定义、推理与训练的标准库。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 35k</span><span class="meta-item">Apache License 2.0</span><a class="meta-home" href="https://huggingface.co/transformers" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>audio</li><li>deep-learning</li><li>deepseek</li><li>gemma</li><li>glm</li></ul>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="rag">
          <h3 class="sub-head">RAG、记忆与评测<span class="sub-count">6</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-firecrawl-firecrawl">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">F</span><img class="avatar-img" src="https://github.com/firecrawl.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/firecrawl/firecrawl" target="_blank" rel="noopener">firecrawl/firecrawl</a>
                  <span class="repo-stars">★ 195.2k</span>
                </div>
                <p class="repo-desc">把网页和文档抓成 LLM 可用的 Markdown 数据。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 10.3k</span><span class="meta-item">GNU Affero General Public License v3.0</span><a class="meta-home" href="https://firecrawl.dev" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>ai-agents</li><li>ai-crawler</li><li>ai-scraping</li><li>ai-search</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-run-llama-llama-index">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">R</span><img class="avatar-img" src="https://github.com/run-llama.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/run-llama/llama_index" target="_blank" rel="noopener">run-llama/llama_index</a>
                  <span class="repo-stars">★ 52.7k</span>
                </div>
                <p class="repo-desc">文档解析、索引、RAG 与 Agent 工作流的工具箱。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 8.4k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://developers.llamaindex.ai" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>agents</li><li>application</li><li>data</li><li>fine-tuning</li><li>framework</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-mem0ai-mem0">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">M</span><img class="avatar-img" src="https://github.com/mem0ai.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/mem0ai/mem0" target="_blank" rel="noopener">mem0ai/mem0</a>
                  <span class="repo-stars">★ 67.8k</span>
                </div>
                <p class="repo-desc">可插拔的长期记忆层，适合聊天助手与个人 Agent。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 8k</span><span class="meta-item">Apache License 2.0</span><a class="meta-home" href="https://mem0.ai" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>agentic-memory</li><li>agentic-memory-system</li><li>agents</li><li>ai</li><li>ai-agents</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-langfuse-langfuse">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">L</span><img class="avatar-img" src="https://github.com/langfuse.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/langfuse/langfuse" target="_blank" rel="noopener">langfuse/langfuse</a>
                  <span class="repo-stars">★ 36.4k</span>
                </div>
                <p class="repo-desc">Trace、Eval 与 Prompt 管理，可开源自托管。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 4.1k</span><a class="meta-home" href="https://langfuse.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>analytics</li><li>autogen</li><li>evaluation</li><li>langchain</li><li>large-language-models</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-promptfoo-promptfoo">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">P</span><img class="avatar-img" src="https://github.com/promptfoo.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/promptfoo/promptfoo" target="_blank" rel="noopener">promptfoo/promptfoo</a>
                  <span class="repo-stars">★ 26.4k</span>
                </div>
                <p class="repo-desc">声明式评测、红队测试与 CI，支持多模型对比。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 2.6k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://promptfoo.dev" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ci</li><li>ci-cd</li><li>cicd</li><li>evaluation</li><li>evaluation-framework</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-berriai-litellm">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">B</span><img class="avatar-img" src="https://github.com/BerriAI.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/BerriAI/litellm" target="_blank" rel="noopener">BerriAI/litellm</a>
                  <span class="repo-stars">★ 62k</span>
                </div>
                <p class="repo-desc">统一 100+ 模型 API，支持成本追踪、fallback 与预算。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 12.7k</span><a class="meta-home" href="https://docs.litellm.ai/docs/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai-gateway</li><li>anthropic</li><li>azure-openai</li><li>bedrock</li><li>gateway</li></ul>
              </div>
            </li>
          </ul>
        </section>
      </section>

      <!-- ========== Ⅳ 提效率 ========== -->
      <section class="cat" data-cat="tools">
        <h2 class="cat-head"><span class="cat-num">Ⅳ</span>提效率</h2>
        <p class="cat-note">工具不决定上限，但决定你每天浪费多少时间。</p>

        <section class="sub" data-sub="editor">
          <h3 class="sub-head">编辑器与终端<span class="sub-count">2</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-microsoft-vscode">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">M</span><img class="avatar-img" src="https://github.com/microsoft.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/microsoft/vscode" target="_blank" rel="noopener">microsoft/vscode</a>
                  <span class="repo-stars">★ 194.3k</span>
                </div>
                <p class="repo-desc">VS Code 源码仓库（Code - OSS）。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 45.3k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://code.visualstudio.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>editor</li><li>electron</li><li>microsoft</li><li>typescript</li><li>visual-studio-code</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-microsoft-terminal">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">M</span><img class="avatar-img" src="https://github.com/microsoft.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/microsoft/terminal" target="_blank" rel="noopener">microsoft/terminal</a>
                  <span class="repo-stars">★ 105.2k</span>
                </div>
                <p class="repo-desc">多标签、分屏、GPU 渲染的现代终端。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#f34b7d"></i>C++</span><span class="meta-item">⑂ 9.7k</span><span class="meta-item">MIT License</span></div>
                <ul class="repo-topics"><li>cmd</li><li>command-line</li><li>console</li><li>contributions-welcome</li><li>good-first-issue</li></ul>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="devkit">
          <h3 class="sub-head">开发工具链<span class="sub-count">3</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-devtoys-app-devtoys">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">D</span><img class="avatar-img" src="https://github.com/DevToys-app.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/DevToys-app/DevToys" target="_blank" rel="noopener">DevToys-app/DevToys</a>
                  <span class="repo-stars">★ 32.1k</span>
                </div>
                <p class="repo-desc">开发者转换、格式化、正则与哈希工具箱。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#178600"></i>C#</span><span class="meta-item">⑂ 1.8k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://devtoys.app/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>blazor</li><li>cross-platform</li><li>csharp</li><li>desktop</li><li>desktop-app</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-usebruno-bruno">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">U</span><img class="avatar-img" src="https://github.com/usebruno.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/usebruno/bruno" target="_blank" rel="noopener">usebruno/bruno</a>
                  <span class="repo-stars">★ 47.8k</span>
                </div>
                <p class="repo-desc">离线、Git 友好的 API 客户端。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#f1e05a"></i>JavaScript</span><span class="meta-item">⑂ 3k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://www.usebruno.com/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>api-client</li><li>api-testing</li><li>automation</li><li>developer-tools</li><li>git</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-n8n-io-n8n">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">N</span><img class="avatar-img" src="https://github.com/n8n-io.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/n8n-io/n8n" target="_blank" rel="noopener">n8n-io/n8n</a>
                  <span class="repo-stars">★ 208.5k</span>
                </div>
                <p class="repo-desc">可视化工作流自动化平台，可写 JS/Python 节点，支持自托管。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 61.2k</span><a class="meta-home" href="https://n8n.io" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>apis</li><li>automation</li><li>cli</li><li>data-flow</li></ul>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="desktop">
          <h3 class="sub-head">桌面效率<span class="sub-count">5</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-microsoft-powertoys">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">M</span><img class="avatar-img" src="https://github.com/microsoft.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/microsoft/PowerToys" target="_blank" rel="noopener">microsoft/PowerToys</a>
                  <span class="repo-stars">★ 139.9k</span>
                </div>
                <p class="repo-desc">微软 Windows 效率工具集，含窗口布局、批量重命名等。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#555555"></i>C</span><span class="meta-item">⑂ 8.6k</span><span class="meta-item">MIT License</span></div>
                <ul class="repo-topics"><li>advanced-paste</li><li>color-picker</li><li>command-palette</li><li>desktop</li><li>fancyzones</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-clash-verge-rev-clash-verge-rev">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">C</span><img class="avatar-img" src="https://github.com/clash-verge-rev.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/clash-verge-rev/clash-verge-rev" target="_blank" rel="noopener">clash-verge-rev/clash-verge-rev</a>
                  <span class="repo-stars">★ 153.8k</span>
                </div>
                <p class="repo-desc">基于 Tauri 的 Clash 桌面客户端，支持订阅与规则管理。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#dea584"></i>Rust</span><span class="meta-item">⑂ 11k</span><span class="meta-item">GNU General Public License v3.0</span><a class="meta-home" href="https://www.clashverge.dev" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>clash</li><li>clash-meta</li><li>clash-verge</li><li>linux</li><li>mac</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-flow-launcher-flow-launcher">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">F</span><img class="avatar-img" src="https://github.com/Flow-Launcher.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/Flow-Launcher/Flow.Launcher" target="_blank" rel="noopener">Flow-Launcher/Flow.Launcher</a>
                  <span class="repo-stars">★ 15.9k</span>
                </div>
                <p class="repo-desc">快速启动与文件搜索工具。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#178600"></i>C#</span><span class="meta-item">⑂ 663</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://flowlauncher.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>alfred</li><li>application-launcher</li><li>desktop</li><li>finder</li><li>flow-launcher</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-sharex-sharex">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">S</span><img class="avatar-img" src="https://github.com/ShareX.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/ShareX/ShareX" target="_blank" rel="noopener">ShareX/ShareX</a>
                  <span class="repo-stars">★ 40.4k</span>
                </div>
                <p class="repo-desc">截图、录屏、OCR 与上传一体化。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#178600"></i>C#</span><span class="meta-item">⑂ 4k</span><span class="meta-item">GNU General Public License v3.0</span><a class="meta-home" href="https://getsharex.com" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>avalonia</li><li>capture</li><li>color-picker</li><li>csharp</li><li>dropbox</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-keepassxreboot-keepassxc">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">K</span><img class="avatar-img" src="https://github.com/keepassxreboot.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/keepassxreboot/keepassxc" target="_blank" rel="noopener">keepassxreboot/keepassxc</a>
                  <span class="repo-stars">★ 29.5k</span>
                </div>
                <p class="repo-desc">离线密码管理器，支持浏览器插件与 TOTP。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#f34b7d"></i>C++</span><span class="meta-item">⑂ 2k</span><a class="meta-home" href="https://keepassxc.org/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>cross-platform</li><li>hacktoberfest</li><li>keepass</li><li>keepassxc</li><li>linux</li></ul>
              </div>
            </li>
          </ul>
        </section>
      </section>

      <!-- ========== Ⅴ 上线跑 ========== -->
      <section class="cat" data-cat="ship">
        <h2 class="cat-head"><span class="cat-num">Ⅴ</span>上线跑</h2>
        <p class="cat-note">只在 localhost 跑通不算本事，能部署、能维护才算。</p>

        <section class="sub" data-sub="ops">
          <h3 class="sub-head">容器与运维<span class="sub-count">1</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-k3s-io-k3s">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">K</span><img class="avatar-img" src="https://github.com/k3s-io.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/k3s-io/k3s" target="_blank" rel="noopener">k3s-io/k3s</a>
                  <span class="repo-stars">★ 34.3k</span>
                </div>
                <p class="repo-desc">单二进制轻量 K8s，一条命令起集群。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#00ADD8"></i>Go</span><span class="meta-item">⑂ 2.8k</span><span class="meta-item">Apache License 2.0</span><a class="meta-home" href="https://k3s.io" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>k8s</li><li>kubernetes</li></ul>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="selfhost">
          <h3 class="sub-head">自托管与媒体<span class="sub-count">4</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-immich-app-immich">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">I</span><img class="avatar-img" src="https://github.com/immich-app.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/immich-app/immich" target="_blank" rel="noopener">immich-app/immich</a>
                  <span class="repo-stars">★ 117.2k</span>
                </div>
                <p class="repo-desc">自托管 Google Photos 替代，支持手机备份与相册共享。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3178c6"></i>TypeScript</span><span class="meta-item">⑂ 7.3k</span><span class="meta-item">GNU Affero General Public License v3.0</span><a class="meta-home" href="https://immich.app" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>backup-tool</li><li>flutter</li><li>google-photos</li><li>google-photos-alternative</li><li>javascript</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-paperless-ngx-paperless-ngx">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">P</span><img class="avatar-img" src="https://github.com/paperless-ngx.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/paperless-ngx/paperless-ngx" target="_blank" rel="noopener">paperless-ngx/paperless-ngx</a>
                  <span class="repo-stars">★ 47.1k</span>
                </div>
                <p class="repo-desc">扫描、OCR、归档与全文搜索文档。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 3.3k</span><span class="meta-item">GNU General Public License v3.0</span><a class="meta-home" href="http://docs.paperless-ngx.com/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>angular</li><li>archiving</li><li>django</li><li>dms</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-dani-garcia-vaultwarden">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">D</span><img class="avatar-img" src="https://github.com/dani-garcia.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/dani-garcia/vaultwarden" target="_blank" rel="noopener">dani-garcia/vaultwarden</a>
                  <span class="repo-stars">★ 69.6k</span>
                </div>
                <p class="repo-desc">轻量 Bitwarden 兼容密码服务器。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#dea584"></i>Rust</span><span class="meta-item">⑂ 3.4k</span><span class="meta-item">GNU Affero General Public License v3.0</span></div>
                <ul class="repo-topics"><li>bitwarden</li><li>bitwarden-rs</li><li>docker</li><li>rocket</li><li>rust</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-jellyfin-jellyfin">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">J</span><img class="avatar-img" src="https://github.com/jellyfin.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/jellyfin/jellyfin" target="_blank" rel="noopener">jellyfin/jellyfin</a>
                  <span class="repo-stars">★ 58.6k</span>
                </div>
                <p class="repo-desc">自托管媒体服务器，管理电影、剧集与音乐。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#178600"></i>C#</span><span class="meta-item">⑂ 5.7k</span><span class="meta-item">GNU General Public License v2.0</span><a class="meta-home" href="https://jellyfin.org" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>csharp</li><li>dotnet</li><li>hacktoberfest</li><li>jellyfin</li></ul>
              </div>
            </li>
          </ul>
        </section>
      </section>

      <!-- ========== Ⅵ 长本事 ========== -->
      <section class="cat" data-cat="grow">
        <h2 class="cat-head"><span class="cat-num">Ⅵ</span>长本事</h2>
        <p class="cat-note">技术会过时，学习方法和视野不会。</p>

        <section class="sub" data-sub="interview">
          <h3 class="sub-head">面试与系统设计<span class="sub-count">2</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-snailclimb-javaguide">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">S</span><img class="avatar-img" src="https://github.com/Snailclimb.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/Snailclimb/JavaGuide" target="_blank" rel="noopener">Snailclimb/JavaGuide</a>
                  <span class="repo-stars">★ 159.2k</span>
                </div>
                <p class="repo-desc">Java 后端面试与学习指南。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#f1e05a"></i>JavaScript</span><span class="meta-item">⑂ 46.1k</span><span class="meta-item">Apache License 2.0</span><a class="meta-home" href="https://javaguide.cn" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>agent</li><li>ai</li><li>context-engineering</li><li>deepseek</li><li>interview</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-donnemartin-system-design-primer">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">D</span><img class="avatar-img" src="https://github.com/donnemartin.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/donnemartin/system-design-primer" target="_blank" rel="noopener">donnemartin/system-design-primer</a>
                  <span class="repo-stars">★ 375.5k</span>
                </div>
                <p class="repo-desc">大规模系统设计入门与面试资料。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 59k</span></div>
                <ul class="repo-topics"><li>design</li><li>design-patterns</li><li>design-system</li><li>development</li><li>interview</li></ul>
              </div>
            </li>
          </ul>
        </section>

        <section class="sub" data-sub="roadmap">
          <h3 class="sub-head">学习路线与资源<span class="sub-count">3</span></h3>
          <ul class="repo-list">
            <li class="repo-item" id="r-f-prompts-chat">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">F</span><img class="avatar-img" src="https://github.com/f.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/f/prompts.chat" target="_blank" rel="noopener">f/prompts.chat</a>
                  <span class="repo-stars">★ 174.5k</span>
                </div>
                <p class="repo-desc">开源提示词库，按角色和场景分类。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#e34c26"></i>HTML</span><span class="meta-item">⑂ 22.3k</span><a class="meta-home" href="https://prompts.chat" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>ai</li><li>artificial-intelligence</li><li>awesome-list</li><li>chatgpt</li><li>chatgpt-prompts</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-public-apis-public-apis">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">P</span><img class="avatar-img" src="https://github.com/public-apis.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/public-apis/public-apis" target="_blank" rel="noopener">public-apis/public-apis</a>
                  <span class="repo-stars">★ 492k</span>
                </div>
                <p class="repo-desc">免费公开 API 清单，按分类收录。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#3572A5"></i>Python</span><span class="meta-item">⑂ 54.8k</span><span class="meta-item">MIT License</span><a class="meta-home" href="https://APILayer.com/?utm_source=Github&amp;utm_medium=Referral&amp;utm_campaign=Public-apis-repo" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>api</li><li>apis</li><li>dataset</li><li>development</li><li>free</li></ul>
              </div>
            </li>
            <li class="repo-item" id="r-datatalksclub-data-engineering-zoomcamp">
              <span class="repo-avatar" aria-hidden="true"><span class="avatar-letter">D</span><img class="avatar-img" src="https://github.com/DataTalksClub.png?size=80" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"></span>
              <div class="repo-body">
                <div class="repo-line">
                  <a class="repo-name" href="https://github.com/DataTalksClub/data-engineering-zoomcamp" target="_blank" rel="noopener">DataTalksClub/data-engineering-zoomcamp</a>
                  <span class="repo-stars">★ 46.4k</span>
                </div>
                <p class="repo-desc">免费 9 周数据工程训练营，含作业与项目。</p>
                <div class="repo-meta"><span class="meta-item"><i class="lang-dot" style="--c:#DA5B0B"></i>Jupyter Notebook</span><span class="meta-item">⑂ 9k</span><a class="meta-home" href="https://courses.datatalks.club/register/de-zoomcamp/" target="_blank" rel="noopener">官网</a></div>
                <ul class="repo-topics"><li>course</li><li>data-engineering</li><li>dbt</li><li>docker</li><li>free</li></ul>
              </div>
            </li>
          </ul>
        </section>
      </section>
    </main>
  </div>
</div>

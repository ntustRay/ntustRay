<p>
  <img src="assets/header.svg" alt="MingRay, Full-Stack Engineer. React, TypeScript, Node.js, SQL." width="100%" />
</p>

[Blog](https://ntustray.github.io/mr-blog/) &nbsp;&nbsp; [Projects](https://github.com/ntustRay?tab=repositories) &nbsp;&nbsp; [npm](https://www.npmjs.com/package/@ntustray/react-datetime-range-picker)

I'm MingRay, a Full-Stack Engineer working with TypeScript, React, Next.js, Canvas, and DuckDB.
My current work involves large datasets and charting: how data is queried, how it reaches the renderer, and how the UI responds to interaction.

Outside work, I build reusable components and small applications, and write about the decisions behind them.

## What I work on

| Area | The problems I spend time on |
| --- | --- |
| Charting and browser data | Query/render boundaries, coordinate transforms, DPR, and the memory cost of keeping data and render caches. |
| React and component APIs | Controlled state, explicit data contracts, validation, and compatibility when consumers or requirements change. |
| Development workflows | Behavior tests, code review, package-consumer checks, and project documentation that people and coding agents can follow. |

I'm also exploring Web Workers and OPFS for browser data pipelines.

## Selected public work

<table>
  <tr>
    <td width="54" valign="top"><img src="assets/calendar.svg" width="32" height="32" alt="" /></td>
    <td>
      <strong><a href="https://github.com/ntustRay/react-datetime-range-picker">React DateTime Range Picker</a></strong>
      <p>A controlled React component for analytics and chart filters.</p>
      <ul>
        <li>Epoch milliseconds as the public value contract; IANA timezones for display and editing.</li>
        <li>Separate draft changes from Apply/commit, with half-open <code>[start, end)</code> range semantics.</li>
        <li>Validation, keyboard workflows, localization, and package-consumer checks for React 18/19 and SSR.</li>
      </ul>
      <p><a href="https://ntustray.github.io/react-datetime-range-picker/">Demo</a> · <a href="https://www.npmjs.com/package/@ntustray/react-datetime-range-picker">npm</a> · <a href="https://github.com/ntustRay/react-datetime-range-picker/blob/main/docs/PUBLIC_API.md">API contract</a> · <a href="https://github.com/ntustRay/react-datetime-range-picker/blob/main/scripts/verify-packed-consumers.mjs">Consumer checks</a></p>
    </td>
  </tr>
</table>

Other projects:

- [Agent Workspace Template](https://github.com/ntustRay/agent-workspace-template): a small `AGENTS.md` and task-workflow template, including [performance review](https://github.com/ntustRay/agent-workspace-template/blob/main/.agents/skills/performance-review/SKILL.md).
- [Markdown Reader](https://github.com/ntustRay/markdown-file-reader): a side project for local Markdown editing, built with Tauri and TypeScript.

## Technical writing

I write in Traditional Chinese, keeping implementation experience separate from source-based research.

- [Bun + Biome：讓 Agent 每次重跑都快一點](https://ntustray.github.io/mr-blog/posts/bun-biome-agent-iteration-compound-time/)  
  Where installation and per-iteration checks add waiting time.
- [模型變強了，還需要 Superpowers 嗎？](https://ntustray.github.io/mr-blog/posts/superpowers-skills-with-stronger-models/)  
  Workflow overhead, external evidence, and when extra process earns its cost.
- [GitLab Orbit 把 Code Context 放進 DuckDB，適合解決哪些搜尋問題？](https://ntustray.github.io/mr-blog/posts/gitlab-orbit-duckdb-code-context/)  
  What a code graph can answer, and what still needs source inspection.

<details>
<summary>Latest posts (updated daily)</summary>

<!-- BLOG:START -->
- [LFM2.5 本機 Agent：跑得快之前，先確認工具真的會動](https://ntustray.github.io/mr-blog/posts/lfm25-local-agent-speed-tool-calling/)
- [Claude Mods 把擴充點放進 Runtime：什麼時候 Skill 已經不夠？](https://ntustray.github.io/mr-blog/posts/claude-mods-harness-runtime/)
- [Gemini 4 Argon 跑了 11 小時，ADK 團隊只接受 2 個優化](https://ntustray.github.io/mr-blog/posts/gemini-4-argon-adk-review/)
- [GitHub 把 Copilot Runtime 改成 80 萬行 Rust：長任務靠什麼撐住？](https://ntustray.github.io/mr-blog/posts/github-copilot-rust-migration-context/)
- [GitLab Orbit 把 Code Context 放進 DuckDB，適合解決哪些搜尋問題？](https://ntustray.github.io/mr-blog/posts/gitlab-orbit-duckdb-code-context/)
<!-- BLOG:END -->

</details>

<details>
<summary>Repository activity and language statistics</summary>

<!-- REPOS:START -->
- [mr-blog](https://github.com/ntustRay/mr-blog) <sub>2026-10-15</sub>
- [agent-workspace-template](https://github.com/ntustRay/agent-workspace-template) — template for new general ai-agent <sub>2026-09-28</sub>
- [markdown-file-reader](https://github.com/ntustRay/markdown-file-reader) — A Tauri-based Markdown reader with dark mode support <sub>2026-09-18</sub>
- [react-datetime-range-picker](https://github.com/ntustRay/react-datetime-range-picker) — A React date-time range picker. <sub>2026-08-15</sub>
- [2026-korea-busan-travel](https://github.com/ntustRay/2026-korea-busan-travel) — The travel instruction <sub>2026-07-30</sub>
<!-- REPOS:END -->

<p>
  <img src="assets/stats.svg" alt="Public GitHub repository statistics" width="48%" />
  <img src="assets/top-langs.svg" alt="Language distribution by source bytes in public original repositories" width="48%" />
</p>

</details>

<!-- UPDATED:START -->
<sub>Updated 2026-10-15 · [Updated daily by GitHub Actions](https://github.com/ntustRay/ntustRay/actions/workflows/update-profile.yml).</sub>
<!-- UPDATED:END -->

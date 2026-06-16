// Command-center chrome on every page: CUI banner + dark grouped sidebar + topbar.
function renderLayout(active){
  const groups = [
    ["DASHBOARD", [["dashboard.html","Dashboard",1]]],
    ["KNOWLEDGE & CONTENT", [["documents.html","Documents",1],["#","Past Performance",0],["#","Templates",0]]],
    ["ANALYSIS", [["compliance.html","Compliance Matrix",1],["bid.html","Bid / No-Bid",1],["assistant.html","AI Assistant",1]]],
    ["WORKFLOW", [["#","Tasks",0],["#","Approvals",0],["#","Reviews",0]]],
    ["ADMIN", [["audit.html","Audit Logs",1],["#","System Settings",0]]],
  ];
  const nav = groups.map(([g,items]) =>
    `<div class="navgroup">${g}</div>` + items.map(([href,label,real]) =>
      `<a class="navlink ${label===active?'active':''} ${real?'':'soon'}" href="${real?href:'#'}">
         <span class="dot"></span>${label}</a>`).join("")
  ).join("");
  document.body.insertAdjacentHTML("afterbegin", `
    <div class="cui">CONTROLLED UNCLASSIFIED INFORMATION // AUTHORIZED USE ONLY</div>
    <div class="app">
      <aside class="sidebar">
        <div class="brand"><span class="logo">II</span><span><b>BidIntel AI</b><small>COMMAND CENTER</small></span></div>
        ${nav}
      </aside>
      <div class="main">
        <div class="topbar">
          <div class="crumb">Home / <b>${active}</b></div>
          <div class="search"><input placeholder="Search opportunities, documents, people…"/></div>
          <div class="user"><span class="avatar">AD</span><div><b style="font-size:13px">Adam Davis</b><small>Proposal Writer</small></div></div>
        </div>
        <main class="content" id="page"></main>
      </div>
    </div>`);
}

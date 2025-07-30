(async function() {

  const sections = document.querySelectorAll(".engineer-section");
  const ids = Array.from(sections)
    .map(el => el.getAttribute("data-engineer-id"))
    .filter(Boolean);

  if (ids.length === 0) {
    console.warn("No engineer IDs found on the page.");
    return;
  }

  const engineers = await Promise.all(ids.map(id =>
    fetch(`/vontive/getEngineerProtected?id=${id}`)
      .then(res => {
        if (!res.ok) throw new Error(`Failed to load ID ${id}: ${res.status}`);
        return res.json();
      })
  ));


  const headers = [
    "Name",
    "jobTitle",
    "education",
    "yearsAtVontive",
    "experience"
  ];

  const escape = str =>
    `"${String(str).replace(/"/g, '""')}"`;

  const rows = engineers.map(e => [
    escape(e.firstName) + " " + escape(e.lastName),
    escape(e.jobTitle),
    escape((e.education || []).join(";")),
    escape(e.yearsAtVontive),
    escape((e.experience || []).join(";"))
  ].join(","));

  const csv = headers.join(",") + "\n" + rows.join("\n");

  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "engineers.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  console.log("Downloaded engineers.csv");
})();

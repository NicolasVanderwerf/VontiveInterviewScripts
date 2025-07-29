(async function() {
  // 1️⃣ collect all IDs
  const sections = document.querySelectorAll(".engineer-section");
  const ids = Array.from(sections)
    .map(el => el.getAttribute("data-engineer-id"))
    .filter(Boolean);

  if (ids.length === 0) {
    console.warn("No engineer IDs found on the page.");
    return;
  }

  // 2️⃣ fetch each engineer’s JSON
  const engineers = await Promise.all(ids.map(id =>
    fetch(`/vontive/getEngineerProtected?id=${id}`)
      .then(res => {
        if (!res.ok) throw new Error(`Failed to load ID ${id}: ${res.status}`);
        return res.json();
      })
  ));

  // 3️⃣ build CSV text
  const headers = [
    "ID",
    "firstName",
    "lastName",
    "jobTitle",
    "education",
    "yearsAtVontive",
    "experience"
  ];

  const escape = str =>
    `"${String(str).replace(/"/g, '""')}"`;

  const rows = engineers.map(e => [
    escape(e.ID),
    escape(e.firstName),
    escape(e.lastName),
    escape(e.jobTitle),
    escape((e.education || []).join(";")),
    escape(e.yearsAtVontive),
    escape((e.experience || []).join(";"))
  ].join(","));

  const csv = headers.join(",") + "\n" + rows.join("\n");

  // 4️⃣ trigger download
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

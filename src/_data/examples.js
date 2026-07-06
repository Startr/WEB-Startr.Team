// Reads the runnable examples at the repo root so the spec's examples page
// renders the literal source of truth — no copy-pasted snippets to drift.
const fs = require("fs");
const path = require("path");

const EXAMPLES_DIR = path.join(__dirname, "..", "..", "examples");

function readTree(dir, base) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) =>
    a.name.localeCompare(b.name)
  )) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...readTree(full, base));
    } else if (/\.(py|yaml|yml|md|csv)$/.test(entry.name)) {
      files.push({
        rel: path.relative(base, full),
        lang: entry.name.endsWith(".py")
          ? "python"
          : entry.name.endsWith(".md")
          ? "markdown"
          : entry.name.endsWith(".csv")
          ? "text"
          : "yaml",
        content: fs.readFileSync(full, "utf-8"),
      });
    }
  }
  return files;
}

module.exports = () => {
  if (!fs.existsSync(EXAMPLES_DIR)) return [];
  return fs
    .readdirSync(EXAMPLES_DIR, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .sort((a, b) => a.name.localeCompare(b.name))
    .map((e) => {
      const dir = path.join(EXAMPLES_DIR, e.name);
      const readme = path.join(dir, "README.md");
      return {
        name: e.name,
        intro: fs.existsSync(readme) ? fs.readFileSync(readme, "utf-8") : "",
        files: readTree(dir, dir).filter((f) => f.rel !== "README.md"),
      };
    });
};

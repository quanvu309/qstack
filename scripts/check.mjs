#!/usr/bin/env node
// Enforces the repo rules in AGENTS.md. Prints every violation and exits 1 if any.

import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repo = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PROMOTED = ["writing", "documents", "design"];
const BUCKETS = [...PROMOTED, "in-progress", "deprecated"];
const errors = [];
const fail = (file, msg) => errors.push(`${relative(repo, file) || "."}: ${msg}`);
const read = (p) => readFileSync(p, "utf8");

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === ".git" || name === "node_modules") continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

function frontmatter(file) {
  const m = read(file).match(/^---\n([\s\S]*?)\n---\n/);
  if (!m) return null;
  return Object.fromEntries(
    m[1].split("\n").map((l) => l.match(/^([\w-]+):\s*(.*)$/)).filter(Boolean).map((x) => [x[1], x[2].trim()]),
  );
}

const plugin = JSON.parse(read(join(repo, ".claude-plugin/plugin.json")));
const readme = read(join(repo, "README.md"));
const shipped = new Set(plugin.skills.map((s) => s.replace(/^\.\//, "")));

for (const s of shipped) {
  if (!existsSync(join(repo, s, "SKILL.md"))) fail(join(repo, ".claude-plugin/plugin.json"), `${s} has no SKILL.md`);
}

for (const bucket of readdirSync(join(repo, "skills"))) {
  const bucketDir = join(repo, "skills", bucket);
  if (!statSync(bucketDir).isDirectory()) continue;
  if (!BUCKETS.includes(bucket)) fail(bucketDir, `unknown bucket; allowed: ${BUCKETS.join(", ")}`);
  const bucketReadme = join(bucketDir, "README.md");
  const bucketText = existsSync(bucketReadme) ? read(bucketReadme) : (fail(bucketReadme, "missing"), "");

  for (const name of readdirSync(bucketDir)) {
    const dir = join(bucketDir, name);
    if (!statSync(dir).isDirectory()) continue;
    const skillFile = join(dir, "SKILL.md");
    const rel = `skills/${bucket}/${name}`;
    const fm = existsSync(skillFile) ? frontmatter(skillFile) : null;
    if (!fm) { fail(skillFile, "missing or has no frontmatter"); continue; }
    if (fm.name !== name) fail(skillFile, `frontmatter name "${fm.name}" must equal folder "${name}"`);
    if (!fm.description) fail(skillFile, "description is empty");
    else if (fm.description.length > 1024) fail(skillFile, "description over 1024 characters");

    const userInvoked = fm["disable-model-invocation"] === "true";
    const yamlFile = join(dir, "agents/openai.yaml");
    if (!existsSync(yamlFile)) fail(yamlFile, "missing");
    else if (/allow_implicit_invocation:\s*false/.test(read(yamlFile)) !== userInvoked) {
      fail(yamlFile, "policy.allow_implicit_invocation: false must match disable-model-invocation: true");
    }

    if (!bucketText.includes(`(./${name}/SKILL.md)`)) fail(bucketReadme, `does not link ${name}`);
    const promoted = PROMOTED.includes(bucket);
    if (shipped.has(rel) !== promoted) fail(join(repo, ".claude-plugin/plugin.json"), `${rel} must ${promoted ? "" : "not "}be listed`);
    if (readme.includes(`(./${rel}/SKILL.md)`) !== promoted) fail(join(repo, "README.md"), `${rel} must ${promoted ? "" : "not "}be linked`);
  }
}

for (const file of walk(repo)) {
  if (!/\.(md|json|ya?ml|mjs|sh|py)$/.test(file)) continue;
  const text = read(file);
  if (text.includes("\u2014")) fail(file, "contains a long dash (U+2014); rewrite the sentence");
  if (text !== text.normalize("NFC")) fail(file, "is not Unicode NFC");
  if (!file.endsWith(".md")) continue;
  for (const [, target] of text.matchAll(/\]\(([^)\s]+)\)/g)) {
    if (/^(https?:|mailto:|#)/.test(target)) continue;
    if (!existsSync(resolve(dirname(file), target.split("#")[0]))) fail(file, `broken link ${target}`);
  }
}

if (errors.length) {
  console.error(errors.join("\n"));
  console.error(`\n${errors.length} problem(s).`);
  process.exit(1);
}
console.log("All checks passed.");

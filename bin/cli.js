#!/usr/bin/env node

/**
 * antigravity-skills CLI
 *
 * Usage:
 *   npx antigravity-skills install          Install all skills to detected tools
 *   npx antigravity-skills install --tool claude
 *   npx antigravity-skills install --tool cursor --tool windsurf
 *   npx antigravity-skills install --project
 *   npx antigravity-skills install --only caveman,blogger
 *   npx antigravity-skills list             List available skills
 *   npx antigravity-skills --help           Show help
 */

const { install, listSkills, TOOLS } = require("../src/installer");
const path = require("path");

const args = process.argv.slice(2);
const command = args[0];

// ─── Parse flags ────────────────────────────────────────────────────────────
function parseFlags(args) {
  const flags = {
    tools: [],
    project: false,
    global: false,
    force: false,
    all: false,
    only: null,
  };

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--project") {
      flags.project = true;
    } else if (arg === "--global") {
      flags.global = true;
    } else if (arg === "--force") {
      flags.force = true;
    } else if (arg === "--all") {
      flags.all = true;
    } else if (arg === "--tool" && args[i + 1]) {
      flags.tools.push(args[++i]);
    } else if (arg === "--only" && args[i + 1]) {
      flags.only = args[++i].split(",").map((s) => s.trim());
    }
  }

  return flags;
}

// ─── Help ───────────────────────────────────────────────────────────────────
function showHelp() {
  console.log(`
  antigravity-skills — Install composable AI agent skills

  USAGE:
    npx antigravity-skills <command> [options]

  COMMANDS:
    install          Install skills to your AI coding tools
    list             List all available skills

  INSTALL OPTIONS:
    --tool <name>    Target a specific tool (can repeat)
                     Supported: antigravity, claude, codex, cursor, windsurf
    --all            Install to every supported tool
    --project        Install to current project directory
    --global         Install to global config directories
    --force          Overwrite existing files
    --only <skills>  Install specific skills (comma-separated)

  EXAMPLES:
    npx antigravity-skills install
    npx antigravity-skills install --tool claude
    npx antigravity-skills install --tool cursor --tool windsurf --project
    npx antigravity-skills install --only caveman,blogger,slidify
    npx antigravity-skills list
  `);
}

// ─── Main ───────────────────────────────────────────────────────────────────
async function main() {
  if (!command || command === "--help" || command === "-h") {
    showHelp();
    return;
  }

  if (command === "list") {
    listSkills();
    return;
  }

  if (command === "install") {
    const flags = parseFlags(args);

    // Default: auto-detect tools if none specified
    if (flags.tools.length === 0 && !flags.all && !flags.project) {
      flags.all = true;
    }

    const skillsRoot = path.join(__dirname, "..", "skills");
    await install({ skillsRoot, ...flags });
    return;
  }

  console.error(`Unknown command: ${command}`);
  console.error("Run 'npx antigravity-skills --help' for usage.");
  process.exit(1);
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});

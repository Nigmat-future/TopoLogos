# Spatial Transcriptomics Skill

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://github.com/yourusername/spatial-transcriptomics-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-OpenCode%20%7C%20Claude%20Code%20%7C%20Codex%20CLI-green)]()

An AI research collaborator for spatial transcriptomics. Not a tool executor, but a thinking partner.

This skill turns your AI assistant into a domain specialist that reasons about spatial transcriptomics workflows, recommends evidence-backed methods, and generates ready-to-run code templates. It does not execute analysis itself. It helps you think through experimental design, method selection, and result interpretation.

## What Makes This Different

| Tool | What It Does | What This Skill Does |
|------|--------------|----------------------|
| ChatSpatial | Answers general questions about spatial methods | Partners through full analysis workflows with context memory |
| SpatialAgent | Executes predefined pipelines | Recommends and explains method choices, lets you decide |
| STAT-agent | Focuses on statistical testing | Covers the full pipeline from QC to cell-cell communication |

This skill is prompt engineering, not a standalone analysis tool. It augments your expertise. It does not replace a bioinformatician.

## Three Thinking Modes

**Aristotle** (default): Proven methods only. Methods must have 2+ years of community validation and peer-reviewed citations. Named for the empiricist who classified all of nature — this mode inherits his systematic rigor. Best for regulated environments or when reproducibility is paramount.

**Plato**: Recent advances from 2024 onward, literature-augmented recommendations. Named for the dialectician who explored every possibility — this mode inherits his breadth. Uses BioMCP to pull the latest publications and enrichment data. Best for research projects pushing methodological boundaries.

**Socrates**: Question-driven reverse design. Starts with your biological question and works backward to experimental design, even if that means crossing into adjacent fields. Named for the gadfly who questioned everything until truth emerged — this mode inherits his relentless curiosity. Best for exploratory or hypothesis-generating work.

## Installation

### OpenCode

Clone into your skills directory:

```bash
git clone https://github.com/yourusername/spatial-transcriptomics-skill.git \
  ~/.opencode/skills/spatial-transcriptomics
```

### Claude Code

```bash
git clone https://github.com/yourusername/spatial-transcriptomics-skill.git \
  ~/.claude/skills/spatial-transcriptomics
```

### Codex CLI

```bash
git clone https://github.com/yourusername/spatial-transcriptomics-skill.git \
  ~/.codex/skills/spatial-transcriptomics
```

Requires the BioMCP tool for literature and gene lookups. Install separately if your agent does not include it.

## Usage Examples

### Example 1: Aristotle Mode

**You:** "I have Visium data from mouse brain. Walk me through the standard pipeline."

**Skill:** Detects Visium platform, enters Aristotle mode, and guides step by step through QC, normalization, clustering, spatial domain detection, and visualization. At each step, it names the recommended method, cites the original paper, and provides a code template with TODO markers for your file paths.

### Example 2: Plato Mode

**You:** "What are the newest methods for cell-type deconvolution in 2025?"

**Skill:** Switches to Plato mode, queries BioMCP for articles from 2024 onward, compares recent methods against your data characteristics, and recommends the most suitable approach with a summary of trade-offs.

### Example 3: Socrates Mode

**You:** "I want to find microenvironments that predict drug response, but I do not know where to start."

**Skill:** Enters Socrates mode, reframes your question into testable sub-questions, suggests an experimental design that combines spatial transcriptomics with pharmacogenomic data, and outlines a reverse analysis plan.

## FAQ

**Can it run analysis on my data?**

No. This skill generates code templates and reasoning. You run the code in your own Python or R environment.

**What platforms are supported?**

OpenCode, Claude Code, and Codex CLI. The skill uses standard Markdown and YAML frontmatter, so any agent that loads skills from a directory should work.

**How is this different from ChatSpatial?**

ChatSpatial answers questions. This skill walks through complete workflows, remembers context across sessions, and tailors recommendations to your data platform and biological question.

**Do I need to install Python packages?**

Not for the skill itself. The code templates it generates will require Scanpy, Squidpy, or other standard spatial transcriptomics libraries in your analysis environment.

## Contributing

### Add a New Method

Edit `reference/methods-catalog.md`. Include the method name, publication year, citation, recommended platform, and which mode(s) it belongs to. Methods for Aristotle mode must be 2+ years old and have independent validation.

### Propose a New Personality Mode

Open an issue with the mode name, the type of biological question it serves, and how it differs from the existing three. Include at least two example dialogues showing the mode in action.

## License

MIT License. See LICENSE for details.

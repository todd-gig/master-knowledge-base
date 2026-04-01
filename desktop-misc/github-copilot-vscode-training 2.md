# GitHub Copilot in VS Code — Setup, Integration & Complete Feature Reference

> **Purpose:** This document serves as a training reference for VS Code and AI assistants (including Claude) to understand, set up, and operate every feature of GitHub Copilot in VS Code. All tasks, tools, commands, shortcuts, and workflows are itemized below.

---

## Table of Contents

1. [Prerequisites & Setup](#1-prerequisites--setup)
2. [Essential Keyboard Shortcuts](#2-essential-keyboard-shortcuts)
3. [Accessing AI in VS Code](#3-accessing-ai-in-vs-code)
4. [Chat Experience](#4-chat-experience)
5. [Adding Context to Prompts](#5-adding-context-to-prompts)
6. [Built-In Chat Tools (Full Reference)](#6-built-in-chat-tools-full-reference)
7. [Slash Commands (Full Reference)](#7-slash-commands-full-reference)
8. [Chat Participants](#8-chat-participants)
9. [Using Agents](#9-using-agents)
10. [Planning with Agents](#10-planning-with-agents)
11. [Customizing Your Chat Experience](#11-customizing-your-chat-experience)
12. [Editor AI Features](#12-editor-ai-features)
13. [Source Control & Issues](#13-source-control--issues)
14. [Code Review (Experimental)](#14-code-review-experimental)
15. [Search & Settings](#15-search--settings)
16. [Generating Tests](#16-generating-tests)
17. [Debugging & Fixing Problems](#17-debugging--fixing-problems)
18. [Scaffolding a New Project](#18-scaffolding-a-new-project)
19. [Terminal Integration](#19-terminal-integration)
20. [Python & Notebook Support](#20-python--notebook-support)
21. [MCP Server Integration](#21-mcp-server-integration)
22. [Third-Party Agents](#22-third-party-agents)
23. [Best Practices & Tips Summary](#23-best-practices--tips-summary)

---

## 1. Prerequisites & Setup

### 1.1 Get a Copilot Subscription
- **Free plan:** Sign up at github.com/copilot — includes a monthly limit of inline suggestions and chat interactions.
- **Paid plans:** GitHub Copilot Pro / Business / Enterprise for unlimited usage.

### 1.2 Install VS Code
- Download from: https://code.visualstudio.com
- Supported platforms: Windows, macOS, Linux, VS Code for the Web, Raspberry Pi.

### 1.3 Install the GitHub Copilot Extension
1. Open VS Code.
2. Press `Cmd+Shift+X` (macOS) / `Ctrl+Shift+X` (Windows/Linux) to open Extensions.
3. Search for **"GitHub Copilot"**.
4. Install both:
   - **GitHub Copilot** (inline suggestions)
   - **GitHub Copilot Chat** (chat features)

### 1.4 Sign In to GitHub
1. After install, VS Code will prompt you to sign in to GitHub.
2. Follow the OAuth flow in your browser.
3. Grant the required permissions to complete authorization.

### 1.5 Verify Installation
- Copilot icon appears in the VS Code status bar (bottom right).
- Open a file and start typing — inline suggestions should appear.
- Press `Ctrl+Cmd+I` (macOS) to open the Chat view.

### 1.6 Enterprise / Organization Setup
- Enterprise policies are managed at the organization level.
- Admins can configure AI settings, extensions, telemetry, and updates via enterprise policies.
- The `chat.tools.global.autoApprove` setting is managed at the organization level.

---

## 2. Essential Keyboard Shortcuts

> macOS shortcuts listed. For Windows/Linux, substitute `Cmd` → `Ctrl` and `Option` → `Alt`.

| Shortcut | Action |
|---|---|
| `Ctrl+Cmd+I` | Open the Chat view (Secondary Side Bar) |
| `Cmd+I` | Start inline chat in the editor or terminal |
| `Cmd+I` (hold) | Start inline voice chat |
| `Cmd+I` in Chat view | Enter voice chat prompt |
| `Cmd+N` in Chat view | Start a new chat session |
| `Shift+Cmd+I` | Switch to using agents in the Chat view |
| `Shift+Option+Cmd+L` | Open Quick Chat |
| `Option+Cmd+.` | Open the model picker to select a different AI model |
| `Tab` | Accept inline suggestion or navigate to the next edit suggestion |
| `Escape` | Dismiss inline suggestion |
| `F2` | Get AI-powered rename suggestions for symbols |

---

## 3. Accessing AI in VS Code

Copilot is available through multiple entry points:

### Chat Entry Points
| Entry Point | How to Access | Use Case |
|---|---|---|
| **Chat view** | `Ctrl+Cmd+I` | Keep an ongoing conversation in the Side Bar |
| **Inline Chat (editor/terminal)** | `Cmd+I` | Ask questions while staying in coding flow |
| **Quick Chat** | `Shift+Option+Cmd+L` | Quick questions without leaving your task |

### Editor AI Entry Points
| Feature | Description |
|---|---|
| **Inline suggestions** | Appear automatically as you type; press `Tab` to accept |
| **Code comment prompts** | Write a comment as a natural language prompt; Copilot generates code below it |
| **Edit context menu** | Right-click in editor → access AI actions (explain, fix, generate tests, review) |
| **Code Actions (lightbulb)** | Click the lightbulb icon to fix linting/compiler errors with AI |

### Task-Specific Smart Actions (Available Across VS Code)
- Generate commit messages
- Generate pull request titles and descriptions
- Fix testing errors
- Semantic file search suggestions

---

## 4. Chat Experience

Copilot Chat allows natural language conversations for coding help: explaining code, refactoring, implementing features, and more.

### Chat View Actions

| Action | Shortcut / Method | Description |
|---|---|---|
| Open Chat view | `Ctrl+Cmd+I` | Opens in the Secondary Side Bar |
| Start inline chat | `Cmd+I` | Chat inside editor or terminal |
| Open Quick Chat | `Shift+Option+Cmd+L` | Lightweight chat popup |
| New chat session | `Cmd+N` | Starts a fresh conversation |
| Toggle agents | (unassigned) | Switch between available agents |
| Model picker | `Option+Cmd+.` | Select a different AI model |
| Context window indicator | Visual in chat input | Shows token usage; hover for breakdown by category |
| Add Context | Click "Add Context..." | Attach files, symbols, selections, etc. |
| Edit previous prompt | Click Edit (✎) | Edit a prior prompt and revert changes |
| Access chat history | Click History icon | Browse past chat sessions |
| Queue/steer request | Send follow-up while running | Queue, steer, or stop+send the current request |
| Voice input | Click Voice icon | Speak your prompt; response is read aloud |
| KaTeX math rendering | Enable `chat.math.enabled` | Renders mathematical equations in chat |
| Mermaid diagram rendering | Enable `mermaid-chat.enabled` | Renders Mermaid diagrams in chat |

### Syntax Reference in Chat
| Syntax | Purpose |
|---|---|
| `#mention` | Reference a tool or chat variable to add context |
| `@mention` | Reference a chat participant (e.g., `@github`, `@terminal`, `@vscode`) |
| `/command` | Run a slash command (e.g., `/fix`, `/tests`, `/explain`) |

---

## 5. Adding Context to Prompts

Providing context improves response accuracy. Use the following methods:

| Method | Description |
|---|---|
| **Add Context button** | Opens a Quick Pick to select files, symbols, editor selection, terminal selection, etc. |
| **Drag & drop files** | Drag from Explorer or Search view, or drag an editor tab onto Chat |
| **Drag & drop folders** | Drag a folder onto Chat to attach all files within it |
| **Drag & drop problems** | Drag an item from the Problems panel into Chat |
| `#<file|folder|symbol>` | Type `#` followed by a name to add it as context |
| `#-mention` | Type `#` followed by a specific tool name to invoke that tool's context |

### Tips for Context
- Use `#mentions` liberally to anchor responses to your codebase.
- Be specific and keep prompts simple.
- Ask follow-up questions to refine results.

---

## 6. Built-In Chat Tools (Full Reference)

Tools extend agent capabilities. Use them via `#toolname` in chat.

### Agent Tools
| Tool | Description |
|---|---|
| `#agent` | (Tool set) Delegate tasks to other agents |
| `#agent/runSubagent` | Run a task in an isolated subagent context — improves context management of the main agent thread |

### Browser Tools (Experimental)
| Tool | Description |
|---|---|
| `#browser` | (Tool set) Interact with the integrated browser |
| *(capabilities)* | Navigate, read page content, take screenshots, click, type, hover, drag, handle dialogs |
| *Enable with:* | `workbench.browser.enableChatTools` setting |

### Edit Tools
| Tool | Description |
|---|---|
| `#edit` | (Tool set) Enable workspace modifications |
| `#edit/createDirectory` | Create a new directory in the workspace |
| `#edit/createFile` | Create a new file in the workspace |
| `#edit/editFiles` | Apply edits to workspace files |
| `#edit/editNotebook` | Make edits to a notebook |

### Execute Tools
| Tool | Description |
|---|---|
| `#execute` | (Tool set) Execute code and applications on your machine |
| `#execute/createAndRunTask` | Create and run a new task in the workspace |
| `#execute/getTerminalOutput` | Get output from running a terminal command |
| `#execute/runInTerminal` | Run a shell command in the integrated terminal |
| `#execute/runNotebookCell` | Run a notebook cell |
| `#execute/testFailure` | Get unit test failure information for diagnosing tests |

### Workspace Creation Tool
| Tool | Description |
|---|---|
| `#newWorkspace` | Create a new workspace |

### Read Tools
| Tool | Description |
|---|---|
| `#read` | (Tool set) Read files in your workspace |
| `#read/getNotebookSummary` | Get the list of notebook cells and their details |
| `#read/problems` | Add workspace issues from the Problems panel as context |
| `#read/readFile` | Read the content of a file |
| `#read/readNotebookCellOutput` | Read output from a notebook cell execution |
| `#read/terminalLastCommand` | Get the last run terminal command and its output |
| `#read/terminalSelection` | Get the current terminal selection |

### Search Tools
| Tool | Description |
|---|---|
| `#search` | (Tool set) Search for files in the workspace |
| `#search/changes` | List source control changes |
| `#search/codebase` | Semantic code search to find relevant context automatically |
| `#search/fileSearch` | Search for files using glob patterns; returns paths |
| `#search/listDirectory` | List files in a directory |
| `#search/textSearch` | Find text in files |
| `#search/usages` | Combined "Find All References", "Find Implementation", and "Go to Definition" |

### Utility Tools
| Tool | Description |
|---|---|
| `#selection` | Get the current editor selection (only when text is selected) |
| `#todos` | Track implementation and progress with a todo list |
| `#vscode/askQuestions` | Enables the agent to ask clarifying questions via an interactive questions carousel |
| `#vscode/extensions` | Search for and ask about VS Code extensions |
| `#vscode/getProjectSetupInfo` | Get instructions and configuration for scaffolding different project types |
| `#vscode/installExtension` | Install a VS Code extension |
| `#vscode/runCommand` | Run a VS Code command. Example: "Enable zen mode `#runCommand`" |
| `#vscode/VSCodeAPI` | Ask about VS Code functionality and extension development |

### Web Tools
| Tool | Description |
|---|---|
| `#web` | (Tool set) Access web content |
| `#web/fetch` | Fetch content from a given web page. Example: "Summarize `#web/fetch code.visualstudio.com/updates`" |

---

## 7. Slash Commands (Full Reference)

Slash commands are shortcuts for common tasks. Type `/` in the chat input to use them.

### Code Commands
| Command | Description |
|---|---|
| `/doc` | Generate code documentation comments (from editor inline chat) |
| `/explain` | Explain a code block, file, or programming concept |
| `/fix` | Get suggestions to fix a code block or resolve compiler/linting errors |
| `/tests` | Generate tests for selected or all methods/functions in the editor |
| `/setupTests` | Get a recommendation for a testing framework, setup steps, and VS Code testing extension suggestions |

### Session Management Commands
| Command | Description |
|---|---|
| `/clear` | Start a new chat session |
| `/compact` | Compact the conversation by summarizing it — useful when context window is filling up |
| `/fork` | Fork the current chat session into a new independent session that inherits full conversation history |

### Debugging Commands
| Command | Description |
|---|---|
| `/debug` | Show the Chat Debug view to inspect chat logs |
| `/troubleshoot` | Analyze agent debug logs for the current session. Example: `/troubleshoot how many tokens did I use?` |
| *(Requires:)* | `github.copilot.chat.agentDebugLog.enabled` setting |

### Scaffold Commands
| Command | Description |
|---|---|
| `/new` | Scaffold a new VS Code workspace or file using natural language. Preview before creating. Example: `/new Express app using typescript and svelte` |
| `/newNotebook` | Generate a new Jupyter notebook. Example: `/newNotebook get census data and preview key insights with Seaborn` |

### Planning Commands
| Command | Description |
|---|---|
| `/plan` | Create a detailed implementation plan: research requirements, ask clarifying questions, generate structured steps |
| `/search` | Generate a search query for the Search view using natural language |
| `/startDebugging` | Generate a `launch.json` debug configuration and start a debugging session |

### Customization Commands
| Command | Description |
|---|---|
| `/agents` | Configure custom agents |
| `/hooks` | Configure hooks |
| `/instructions` | Configure custom instructions |
| `/prompts` | Configure reusable prompt files |
| `/skills` | Configure agent skills |

### AI-Assisted Generation Commands (Agent Mode)
| Command | Description |
|---|---|
| `/create-prompt` | Generate a prompt file with AI assistance |
| `/create-instruction` | Generate an instructions file with AI assistance |
| `/create-skill` | Generate an agent skill with AI assistance |
| `/create-agent` | Generate a custom agent with AI assistance |
| `/create-hook` | Generate a hook configuration with AI assistance |

### Auto-Approval Commands
| Command | Description |
|---|---|
| `/yolo` / `/autoApprove` | Enable global auto-approval of all tool calls. Shows a warning dialog the first time. (Organization-managed) |
| `/disableYolo` / `/disableAutoApprove` | Disable global auto-approval of all tool calls |

### Custom Commands
| Command | Description |
|---|---|
| `/<skill name>` | Run an agent skill. Example: `/webapp-testing` runs the `webapp-testing.md` skill |
| `/<prompt name>` | Run a reusable prompt file |

### Test-Fix Commands
| Command | Description |
|---|---|
| `/fixTestFailure` | Get suggestions for fixing failing tests |

---

## 8. Chat Participants

Chat participants handle domain-specific requests. Reference them with `@` in your prompt.

| Participant | Description | Example Prompts |
|---|---|---|
| `@github` | Ask about GitHub repositories, issues, pull requests, and more | `@github What are all of the open PRs assigned to me?` |
| `@terminal` | Ask about the integrated terminal or shell commands | `@terminal list the 5 largest files in this workspace` |
| `@vscode` | Ask about VS Code features, settings, and extension APIs | `@vscode how to enable word wrapping?` |

> Extensions can provide additional chat participants beyond these built-in ones.

---

## 9. Using Agents

Agents autonomously plan, implement, and verify changes across multiple files. They combine code editing with tool invocation, monitor outcomes, and iterate to resolve issues.

### Agent Access & Configuration

| Action | Shortcut / Method | Description |
|---|---|---|
| Switch to agents | `Shift+Cmd+I` | Switch to using agents in the Chat view |
| Configure tools | Click Tools icon (⚙) | Select built-in tools, MCP servers, and extension tools |
| Set permission level | Dropdown in chat | Options: **Default Approvals**, **Bypass Approvals**, **Autopilot (Preview)** |
| Auto-approve tools | Setting: `chat.tools.autoApprove` | Enable auto-approval of all tools |
| Auto-approve terminal | Setting: `chat.tools.terminal.autoApprove` | Enable auto-approval of terminal commands |

### Permission Levels Explained
- **Default Approvals:** Agent asks before each tool invocation.
- **Bypass Approvals:** Agent proceeds without asking for most tools.
- **Autopilot (Preview):** Maximum autonomy — agent proceeds without interruption.

### Agent Tips
- Add extra tools (MCP, extensions) to extend agent capabilities.
- Configure custom agents to define how they operate (e.g., read-only planning mode).
- Define custom instructions to guide code generation style.
- Use parallel agents for independent tasks to save time.
- Try third-party agents (Claude Code, OpenAI Codex) for alternative agentic experiences.

---

## 10. Planning with Agents

The Plan agent creates detailed implementation plans before coding begins.

| Feature | Description |
|---|---|
| **Plan agent** | Select "Plan" from the agents dropdown, or use `/plan` — creates detailed plans for complex tasks |
| **Todo list widget** | Tracks progress on complex tasks. Enable with: `chat.tools.todos.showWidget` setting |
| **Memory** | Agents save and recall persistent notes across conversations. Enable/disable: `github.copilot.chat.tools.memory.enabled` |
| **View stored memories** | Run command: `Chat: Show Memory Files` |

### Planning Workflow
1. Use `/plan` or select the Plan agent.
2. Agent researches requirements and asks clarifying questions.
3. Agent generates a structured plan with steps, verification, and decision points.
4. Review and approve the plan.
5. Hand off to an implementation agent to execute.

---

## 11. Customizing Your Chat Experience

Customize how Copilot generates responses to match your team's coding style and workflows.

### Customization Types

| Type | Purpose | How it Works |
|---|---|---|
| **Custom Instructions** | Define guidelines for code generation, code reviews, commit messages | Describes *how* tasks should be done (conditions for the AI) |
| **Reusable Prompt Files** | Define reusable prompts for common tasks | Describes *what* should be done (standalone, runnable prompts) |
| **Custom Agents** | Define how chat operates, which tools it uses, how it interacts with the codebase | Scopes all prompts within defined tool/instruction boundaries |

### Chat Customizations Editor (Preview)
- **Open via:** Click the Configure Chat gear icon in the Chat view, **or** run `Chat: Open Chat Customizations` from the Command Palette.
- Discover, create, and manage all customizations in one place.

### Workspace Instructions File
- Generate or update with: `/init`
- File locations: `copilot-instructions.md` or `AGENTS.md`
- Based on your project structure and coding patterns.

### Customization Tips
- Define language-specific instructions for more accurate code per language.
- Store instructions in your workspace to share them with your team.
- Define reusable prompt files for common tasks to speed up onboarding.

---

## 12. Editor AI Features

### Inline Suggestions
- Appear automatically as you type.
- Copilot considers your existing code and style.
- **Accept:** Press `Tab`
- **Dismiss:** Press `Escape`
- **Navigate to next suggestion:** `Tab` (when reviewing edit suggestions)

### Code Comment Prompts
- Write a comment in natural language; Copilot generates code below it.
- Example:
```python
# write a calculator class with methods for add, subtract, and multiply. Use static methods.
```

### Inline Chat in Editor
- Press `Cmd+I` to open.
- Use natural language, reference `#variables`, and slash commands.
- Stays in the editor flow.

### AI-Powered Rename
- Press `F2` on a symbol to get AI-powered rename suggestions.

### Context Menu AI Actions
- Right-click in editor → **Generate Code** → access:
  - Explain code
  - Fix code
  - Generate tests
  - Review selection

### Code Actions (Lightbulb)
- Click the lightbulb (💡) that appears next to errors.
- Fix linting errors and compiler errors with AI assistance.

### Editor AI Tips
- Use meaningful method/function names for better suggestions.
- Select a code block before using Inline Chat to scope the prompt.
- Attach relevant files or symbols as context for better results.
- Watch for Copilot Code Actions in the editor for automatic fix suggestions.

---

## 13. Source Control & Issues

| Action | Description |
|---|---|
| `#changes` | Add current source control changes as context in your chat prompt |
| **Commit as context** | Add a commit from source control history as chat context |
| **Commit message generation** | Click the sparkle icon in Source Control → generates a commit message from your staged changes |
| **Merge conflicts (Experimental)** | Get AI help resolving Git merge conflicts |
| **Pull request description** | Generate a PR title and description matching your changes |
| `@github` | Ask about issues, PRs, and more across repositories |

### Example Usage
```
@github What are all of the open PRs assigned to me?
@github Show me the recent merged PRs from @dancing-mona
```

---

## 14. Code Review (Experimental)

| Action | How to Access | Description |
|---|---|---|
| **Review Selection (Preview)** | Select code → Right-click → Generate Code > Review | Quick review pass of selected code block |
| **Code Review** | Source Control view → Click "Code Review" button | Deeper review of all uncommitted changes |

- Review feedback appears as **inline comments** in the editor.
- You can **apply the suggestions** directly from the comments.

---

## 15. Search & Settings

| Feature | Setting to Enable | Description |
|---|---|---|
| **AI Settings search** | `workbench.settings.showAISearchToggle` | Include semantic/AI results in the Settings editor |
| **Semantic search (Preview)** | `search.searchView.semanticSearchBehavior` | Include semantic search results in the Search view |

---

## 16. Generating Tests

| Action | Command / Method | Description |
|---|---|---|
| Generate tests | `/tests` | Generate tests for selected or all methods/functions. Appended to existing test file or creates a new one. |
| Setup testing framework | `/setupTests` | Get framework recommendation, setup steps, and VS Code testing extension suggestions |
| Fix failing tests | `/fixTestFailure` | Get suggestions for fixing failing tests |
| Test coverage (Experimental) | Via Coverage view | Generate tests for functions/methods not yet covered |

### Testing Tips
- Specify the testing framework or library you want to use in your prompt.
- Select specific functions before running `/tests` to scope the generation.

---

## 17. Debugging & Fixing Problems

| Action | Command / Method | Description |
|---|---|---|
| Fix code | `/fix` | Suggestions to fix a code block or resolve compiler/linting errors |
| Fix failing tests | `/fixTestFailure` | Suggestions for fixing failing tests |
| Generate debug config | `/startDebugging` (Experimental) | Generate a `launch.json` and start a debugging session from Chat |
| Debug terminal programs | `copilot-debug <command>` | Terminal command — prefix any run command. Example: `copilot-debug python foo.py` |

### Debugging Tips
- Provide details about the type of fix needed (e.g., "optimize memory consumption").
- Watch for Copilot Code Actions (lightbulb) in the editor for automatic fix suggestions.

---

## 18. Scaffolding a New Project

| Action | Command / Method | Description |
|---|---|---|
| Use agent to scaffold | Type in Chat with agent | Natural language project creation. Example: "Create a Svelte web application to track my tasks" |
| Scaffold workspace/file | `/new` | Preview and create a new project or file. Example: `/new Express app using typescript and svelte` |
| Generate Jupyter notebook | `/newNotebook` | Generate a notebook from requirements. Example: `/newNotebook get census data and preview key insights with Seaborn` |

---

## 19. Terminal Integration

| Action | Shortcut / Method | Description |
|---|---|---|
| Terminal inline chat | `Cmd+I` in terminal | Ask about shell commands in natural language. Example: "how many cores on this machine?" |
| Terminal participant | `@terminal` in Chat | Ask questions about the terminal. Example: `@terminal list the 5 largest files in this workspace` |
| Explain terminal output | `@terminal /explain` in Chat | Explain something from the terminal. Example: `@terminal /explain top shell command` |

---

## 20. Python & Notebook Support

| Action | Shortcut / Method | Description |
|---|---|---|
| Inline chat in notebook | `Cmd+I` in notebook | Generate a code cell or Markdown block using AI |
| Attach Jupyter variables | `#variableName` in chat | Attach variables from the Jupyter kernel for more relevant responses |
| Inline chat in Native REPL | `Cmd+I` in Python REPL | Generate and run commands in the Native Python REPL |
| Open Chat view for notebooks | `Ctrl+Cmd+I` | Use agents to make notebook edits |
| Generate notebook | `/newNotebook` | Generate a new Jupyter notebook from natural language requirements |

---

## 21. MCP Server Integration

MCP (Model Context Protocol) extends agent capabilities with external tools and data sources.

| Action | Description |
|---|---|
| **Configure MCP servers** | Add MCP server configurations to extend available tools in agent mode |
| **Use MCP tools** | MCP tools appear alongside built-in tools in the tools picker |
| **MCP configuration** | Managed via the MCP Configuration settings |

### MCP Setup
1. Open VS Code settings or the `mcp-config.json` file.
2. Add your MCP server endpoint and authentication details.
3. In the Chat view → click Tools icon → enable MCP-provided tools.
4. Reference MCP tools in chat prompts using `#toolname`.

---

## 22. Third-Party Agents

Use agents from external providers with your Copilot subscription.

| Agent | Description |
|---|---|
| **Claude Agent (Preview)** | Powered by Anthropic's Claude Agent SDK. Use `/agents`, `/hooks`, and `/memory` slash commands for advanced workflows. |
| **OpenAI Codex** | Alternative agentic coding experience with OpenAI's Codex model |

### Accessing Third-Party Agents
1. In the Chat view, click the agents dropdown (`Shift+Cmd+I`).
2. Select the third-party agent from the list.
3. Use supported slash commands for that agent's advanced features.

---

## 23. Best Practices & Tips Summary

### General Chat
- Be specific and concise in your prompts.
- Ask follow-up questions to refine results.
- Use `#mentions` to ground responses in your actual codebase.
- Choose the agent or participant that fits your specific task.

### Code Generation
- Use meaningful method and function names for better inline suggestions.
- Write descriptive code comments as prompts.
- Select relevant code blocks before invoking inline chat.
- Define language-specific custom instructions for more accurate output.

### Team Collaboration
- Store custom instructions in the workspace (not user settings) to share with the team.
- Define reusable prompt files for common tasks to standardize workflows.
- Use `AGENTS.md` or `copilot-instructions.md` to document agent behavior for the whole team.
- Use `/init` to auto-generate workspace instructions from your project structure.

### Context Management
- Monitor the context window indicator in the Chat input.
- Use `/compact` to summarize long conversations and reclaim context space.
- Use `/fork` to branch off a conversation when exploring a different approach.
- Use `#agent/runSubagent` to isolate complex subtasks and keep the main thread clean.

### Debugging Workflow
1. Use `/fix` on problematic code blocks.
2. Use `copilot-debug <command>` in the terminal to debug run commands directly.
3. Use `/startDebugging` to auto-generate `launch.json` configurations.
4. Watch for lightbulb Code Actions for in-editor fix suggestions.

### Testing Workflow
1. Use `/setupTests` first if no testing framework is configured.
2. Use `/tests` to generate tests for selected functions.
3. Use Test Coverage view (Experimental) to find untested code.
4. Use `/fixTestFailure` when tests break.

### Planning Workflow
1. Start with `/plan` to research and structure complex tasks.
2. Review the generated plan before proceeding.
3. Hand off the approved plan to the implementation agent.
4. Monitor progress via the todo list widget.

---

## Quick Reference Card

```
OPEN CHAT         Ctrl+Cmd+I
INLINE CHAT       Cmd+I
QUICK CHAT        Shift+Option+Cmd+L
NEW SESSION       Cmd+N (in Chat view)
USE AGENTS        Shift+Cmd+I
SWITCH MODEL      Option+Cmd+.
ACCEPT SUGGESTION Tab
DISMISS           Escape
AI RENAME         F2

COMMON SLASH COMMANDS
/explain  /fix  /tests  /doc  /new  /plan
/setupTests  /fixTestFailure  /startDebugging
/newNotebook  /clear  /compact  /fork  /init

CHAT PARTICIPANTS
@github   @terminal   @vscode

KEY TOOLS
#changes  #selection  #codebase  #search/usages
#web/fetch  #read/problems  #execute/runInTerminal
```

---

*Source: [GitHub Copilot in VS Code Cheat Sheet](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features) — Last updated: March 25, 2026*

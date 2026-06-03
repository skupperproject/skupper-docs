# Skupper Documentation Style Guide

## Numbered Lists and Code Blocks

### Indentation Requirements

All continuation content within numbered list items must be indented with exactly 3 spaces. This includes:
- Code fence markers (the triple backticks)
- Code block content
- Labels like "Example output:"
- Any explanatory text that continues from the list item

This 3-space indentation tells the Markdown renderer that the content belongs to that numbered list item.

### Formatting Shell Commands

When showing shell commands in procedural documentation:

1. Use bash code blocks (marked with triple backticks and the bash language identifier)
2. Do NOT include the dollar sign prompt in the command
3. Show only the actual command that users should type
4. The opening and closing fence markers must be indented 3 spaces within numbered lists

### Formatting Command Output

When showing what output users should expect to see:

1. Place the text "Example output:" on its own line before the output block
2. This label must be indented 3 spaces (same as the code fences)
3. Use a text code block (marked with triple backticks and the text language identifier)
4. Include all output lines within the text block
5. Both the opening and closing fence markers must be indented 3 spaces

### Multiple Command/Output Pairs

When demonstrating a sequence of commands and their outputs (such as polling a status command until a condition is met):

1. Show the first command in a bash block
2. Follow with "Example output:" and a text block showing the first result
3. Show the second command in another bash block
4. Follow with "Example output:" and a text block showing the second result
5. All fence markers and labels maintain the 3-space indentation

### Commands Without Output

When you only need to show a command without demonstrating its output, use a single bash code block. No output block is needed.

### YAML and Configuration Files

For YAML configuration files or Kubernetes resources, use yaml as the language identifier instead of bash or text.

### Reference Documentation (refdog directory only)

The reference documentation in the input/refdog directory uses a different format:

- Uses console as the language identifier
- Uses tildes instead of backticks for code fences
- DOES include the dollar sign prompt in commands
- Shows commands and output mixed together in the same block
- May include comment lines starting with hash symbols

This console format is ONLY used in the refdog directory. All procedural documentation uses the bash/text separation described above.

### Key Differences: Procedural vs Reference

Procedural documentation (tutorials, how-to guides):
- Separates commands from output into different blocks
- Commands in bash blocks without dollar sign prompts
- Output in text blocks with "Example output:" labels

Reference documentation (command reference in refdog):
- Shows interactive console sessions as they would appear
- Commands include dollar sign prompts
- Commands and output mixed in the same console block

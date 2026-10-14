---
name: dance
description: Celebrate with an ASCII dance party. Use when something awesome just worked, a deploy succeeded, tests pass, or the user wants to celebrate.
user_invocable: true
---

# /dance

Print a multi-frame ASCII dance celebration directly as chat text. Make it feel like a party.

## Rules

1. Output **8-10 distinct frames** of ASCII dancers, each in its own code block line group
2. Each frame should show **5 dancers** in different poses
3. Use these pose variations freely — mix and match per frame:
   - `\o/` arms up
   - `o/` or `\o` one arm out
   - `_o/` or `\o_` leaning
   - Decorate with `♪` `♫` `★` `🎉`
4. Output as a single markdown code block so alignment is preserved
5. Separate frames with a blank line inside the code block
6. End with a celebration message related to the context (if known) or generic hype
7. Do NOT use the Bash tool — output directly as chat text

## Example

````
```
   ♪           ♫           ♪           ♫           ♪
  \o/         \o/         \o/         \o/         \o/
   |           |           |           |           |
  / \         / \         / \         / \         / \

       ♫           ♪           ♫           ♪
   o/         \o          o/         \o          o/
  /|           |\        /|           |\        /|
  / \         / \       / \         / \        / \

  ★           ★           ★           ★           ★
    \o         \o/          o/        \o/         \o
     |\         |          /|          |           |\
    / \        / \        / \         / \        / \

  🎉          🎉          🎉          🎉          🎉
    _o/        \o_        _o/        \o_        _o/
     |          |          |          |          |
    / \        / \        / \        / \        / \

  ♪ \o/ ♪    \o/ ♪    \o/ ♪    \o/ ♪    \o/ ♪
     |          |          |          |          |
    / \        / \        / \        / \        / \

       ♫    o/    ♫  \o     ♫   o/    ♫  \o     ♫
           /|         |\       /|         |\
           / \       / \      / \        / \

  ★  \o/  ★  \o/  ★  \o/  ★  \o/  ★  \o/  ★
      |        |        |        |        |
     / \      / \      / \      / \      / \

  🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉

            \o/     \o/     \o/     \o/     \o/
             |       |       |       |       |
            / \     / \     / \     / \     / \

         ★  C E L E B R A T I O N   T I M E  ★

  🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉 🎉
```
````

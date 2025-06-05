# 🏰 Idle Dungeon

**Idle Dungeon** is a desktop clicker RPG where players roll for loot, equip powerful gear, and battle through tiered dungeons for increasingly better rewards. This is the first public demo release.

---

## 📦 Features

### ⚔️ Core Gameplay
- Roll loot to collect weapons and armor (first roll is free)
- Equip items to increase ATK/DEF stats
- Enter dungeons to fight enemies and earn XP, coins, and more loot
- Failing a dungeon resets HP, while victory rewards progression

### 🎒 Inventory & Equipment
- Inventory shows item rarity, stats, and icons (🗡/🛡)
- Tooltip popups with item descriptions and details
- Equipment slots show your currently equipped weapon and armor

### 🎲 Loot System
- Extensive loot table with rarity tiers: Common → Legendary
- Each item has stats, type, and description
- Animated loot spin when rolling to simulate a slot machine

### 🏹 Dungeons
- Multiple dungeon tiers with level requirements
- Enemy HP and damage scale with tier
- Rewards increase with each dungeon level

### 📘 Collection Log
- Tracks all possible loot items
- Locked items are blacked out
- Unlocked items show name, description, and rarity
- Displays collection progress as a percentage

### 🧠 Progression
- Leveling system based on dungeon XP
- Scaled XP requirement per level
- Coins are used for loot rolls and vendor purchases
- Potion system allows healing between dungeon runs

### 🛍️ Vendor Shop (Grimrick the Greedy)
- NPC shop with rotating limited-time items
- Shop refreshes every 5 minutes or manually
- Items include potions, XP boosts, and auto-loot upgrades
- Grimrick delivers sarcastic and greedy flavor dialogue

### 💾 Save System
- Auto-saves game progress to a local JSON file
- Fully restores inventory, equipment, stats, and shop state on launch

---

## 📂 Installation & Running

1. Make sure you have **Python 3.10+** installed
2. Clone or download this repository
3. Navigate to the game folder and run:

```bash
python main.py

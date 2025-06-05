from tkinter import *
import random, json, os
import time

# Constants
RARITY_ORDER = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
RARITY_COLORS = {
    "Common": "gray", "Uncommon": "green", "Rare": "blue", "Epic": "purple", "Legendary": "gold"
}
SAVE_FILE = "game_data/save.json"

TIER_DATA = {
    "Tier 1": {"enemy": "Goblin", "hp": (30, 50), "dmg": (5, 10), "xp": 10, "coins": 10, "min_level": 1},
    "Tier 2": {"enemy": "Wraith", "hp": (75, 100), "dmg": (10, 20), "xp": 25, "coins": 25, "min_level": 3},
    "Tier 3": {"enemy": "Dragonling", "hp": (150, 200), "dmg": (20, 35), "xp": 60, "coins": 50, "min_level": 6}
}

LOOT_TABLE = [
    # Common
    {"id": "rusty_sword", "name": "Rusty Sword", "rarity": "Common", "atk": 2, "type": "weapon", "desc": "An old, dull blade."},
    {"id": "leather_armor", "name": "Leather Armor", "rarity": "Common", "def": 1, "type": "armor", "desc": "Worn but reliable."},
    {"id": "wooden_club", "name": "Wooden Club", "rarity": "Common", "atk": 1, "type": "weapon", "desc": "Barely a weapon."},
    {"id": "cloth_robe", "name": "Cloth Robe", "rarity": "Common", "def": 1, "type": "armor", "desc": "Provides minimal protection."},

    # Uncommon
    {"id": "iron_dagger", "name": "Iron Dagger", "rarity": "Uncommon", "atk": 4, "type": "weapon", "desc": "Quick and sharp."},
    {"id": "iron_armor", "name": "Iron Armor", "rarity": "Uncommon", "def": 3, "type": "armor", "desc": "Solid defense."},
    {"id": "hunting_bow", "name": "Hunting Bow", "rarity": "Uncommon", "atk": 3, "type": "weapon", "desc": "For ranged combat."},
    {"id": "padded_vest", "name": "Padded Vest", "rarity": "Uncommon", "def": 2, "type": "armor", "desc": "Comfortable and protective."},

    # Rare
    {"id": "shadow_blade", "name": "Shadow Blade", "rarity": "Rare", "atk": 8, "type": "weapon", "desc": "It whispers in the dark."},
    {"id": "knight_plate", "name": "Knight Plate", "rarity": "Rare", "def": 6, "type": "armor", "desc": "Worn by honored knights."},
    {"id": "arcane_staff", "name": "Arcane Staff", "rarity": "Rare", "atk": 6, "type": "weapon", "desc": "Glows with magical energy."},
    {"id": "scale_mail", "name": "Scale Mail", "rarity": "Rare", "def": 5, "type": "armor", "desc": "Clinks with every step."},

    # Epic
    {"id": "phoenix_blade", "name": "Phoenix Blade", "rarity": "Epic", "atk": 12, "type": "weapon", "desc": "Burns with eternal fire."},
    {"id": "dragonhide_armor", "name": "Dragonhide Armor", "rarity": "Epic", "def": 10, "type": "armor", "desc": "Scales of the ancient."},
    {"id": "storm_scepter", "name": "Storm Scepter", "rarity": "Epic", "atk": 10, "type": "weapon", "desc": "Crackles with lightning."},
    {"id": "guardian_plate", "name": "Guardian Plate", "rarity": "Epic", "def": 9, "type": "armor", "desc": "Forged to protect kings."},

    # Legendary
    {"id": "void_slicer", "name": "Void Slicer", "rarity": "Legendary", "atk": 20, "type": "weapon", "desc": "Cuts through reality itself."},
    {"id": "celestial_armor", "name": "Celestial Armor", "rarity": "Legendary", "def": 18, "type": "armor", "desc": "Woven from starlight."},
    {"id": "doom_reaver", "name": "Doom Reaver", "rarity": "Legendary", "atk": 18, "type": "weapon", "desc": "Hungers for battle."},
    {"id": "ethereal_guard", "name": "Ethereal Guard", "rarity": "Legendary", "def": 16, "type": "armor", "desc": "Shifts with the wind."},
]

def roll_loot_by_rarity():
    roll = random.random()
    if roll < 0.50:
        rarity = "Common"
    elif roll < 0.75:
        rarity = "Uncommon"
    elif roll < 0.90:
        rarity = "Rare"
    elif roll < 0.98:
        rarity = "Epic"
    else:
        rarity = "Legendary"
    candidates = [item for item in LOOT_TABLE if item["rarity"] == rarity]
    return random.choice(candidates) if candidates else random.choice(LOOT_TABLE)


# Tooltip class
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show(self, text, x, y):
        if self.tip_window or not text:
            return
        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x+20}+{y+10}")
        label = Label(tw, text=text, justify='left', background="#ffffe0", relief='solid', borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide(self, _=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Idle Dungeon")
        self.inventory = []
        self.collection_log = set()
        self.equipped_weapon = None
        self.equipped_armor = None
        self.coins = 50 
        self.xp = 0
        self.level = 1
        self.xp_to_next = 20
        self.hp = 100
        self.max_hp = 100
        self.potions = 0
        self.selected_tier = StringVar(value="Tier 1")
        self.tooltip = ToolTip(self.root)
        self.load_game()
        self.create_ui()
        self.first_roll_used = False
        self.vendor_name = "☠ Grimrick the Greedy"
        self.shop_rotation = []
        self.last_shop_refresh = time.time()  # Import time module at top
        self.refresh_shop_items()
        self.auto_loot_enabled = False
        self.auto_loot_cost = 15
        self.root.after(5000, self.auto_loot_tick)  # Auto-loot loop




    def create_ui(self):
        Label(self.root, text="Idle Dungeon").pack()
        self.coin_label = Label(self.root)
        self.coin_label.pack()
        self.hp_label = Label(self.root)
        self.hp_label.pack()
        self.level_label = Label(self.root)
        self.level_label.pack()
        self.potion_label = Label(self.root)
        self.potion_label.pack()
        self.equipped_label = Label(self.root, text="")
        self.equipped_label.pack()
        self.auto_loot_button = Button(self.root, text="Enable Auto-Loot", state=DISABLED, command=self.toggle_auto_loot)
        self.auto_loot_button.pack()


        OptionMenu(self.root, self.selected_tier, *TIER_DATA.keys()).pack()

        Button(self.root, text="Roll Loot", command=self.roll_loot).pack()
        
        self.inventory_list = Listbox(self.root, width=50)
        self.inventory_list.pack()
        Button(self.root, text="Equip Selected", command=self.equip_selected).pack()
        Button(self.root, text="Sell Selected", command=self.sell_selected).pack()
        Button(self.root, text="Bulk Sell", command=self.open_bulk_sell_menu).pack()
        Button(self.root, text="Use Potion", command=self.use_potion).pack()
        Button(self.root, text="Enter Dungeon", command=self.start_dungeon).pack()
        Button(self.root, text="Shop", command=self.open_shop).pack()
        Button(self.root, text="Collection Log", command=self.show_collection).pack()

        self.log = Label(self.root, text="", wraplength=400)
        self.log.pack()
        self.update_ui()

    def update_ui(self):
        self.coin_label.config(text=f"Coins: {self.coins}")
        self.hp_label.config(text=f"HP: {self.hp}/{self.max_hp}")
        self.level_label.config(text=f"Level: {self.level} | XP: {self.xp}/{self.xp_to_next}")
        self.potion_label.config(text=f"Potions: {self.potions}")
        w = self.equipped_weapon["name"] if self.equipped_weapon else "None"
        a = self.equipped_armor["name"] if self.equipped_armor else "None"
        self.equipped_label.config(text=f"Equipped Weapon: {w} | Armor: {a}")

        self.inventory_list.delete(0, END)
        for index, item in enumerate(self.inventory):
            icon = "🗡" if item["type"] == "weapon" else "🛡"
            stat = item.get("atk", item.get("def", 0))
            display = f"{item['name']} [{'W' if item['type'] == 'weapon' else 'A'}] ({item['rarity']}) | {icon} {stat}"
            self.inventory_list.insert(index, display)
            self.inventory_list.itemconfig(index, {'fg': RARITY_COLORS[item["rarity"]]})
        self.bind_tooltips()

        if self.level >= 10:
            self.auto_loot_button.config(state=NORMAL, text="Disable Auto-Loot" if self.auto_loot_enabled else "Enable Auto-Loot")
        else:
            self.auto_loot_button.config(state=DISABLED)


    def bind_tooltips(self):
        def on_motion(event):
            index = self.inventory_list.nearest(event.y)
            if 0 <= index < len(self.inventory):
                item = self.inventory[index]
                text = f"{item['name']}\n{item['desc']}\nRarity: {item['rarity']}\n"
                text += f"{'ATK' if item['type'] == 'weapon' else 'DEF'}: {item.get('atk', item.get('def', 0))}"
                self.tooltip.show(text, event.x_root, event.y_root)
            else:
                self.tooltip.hide()

        def on_leave(event):
            self.tooltip.hide()

        self.inventory_list.bind("<Motion>", on_motion)
        self.inventory_list.bind("<Leave>", on_leave)

    def equip_selected(self):
        selected = self.inventory_list.curselection()
        if not selected: return
        item = self.inventory[selected[0]]
        if item["type"] == "weapon":
            self.equipped_weapon = item
        elif item["type"] == "armor":
            self.equipped_armor = item
        self.log.config(text=f"Equipped {item['name']}")
        self.update_ui()
        self.save_game()

    def toggle_auto_loot(self):
        self.auto_loot_enabled = not self.auto_loot_enabled
        state = "enabled" if self.auto_loot_enabled else "disabled"
        self.log.config(text=f"Auto-Loot {state}.")
        self.update_ui()

    def auto_loot_tick(self):
        if self.auto_loot_enabled and self.level >= 10:
            if self.coins >= self.auto_loot_cost:
                self.coins -= self.auto_loot_cost
                item = roll_loot_by_rarity()
                self.inventory.append(item)
                self.collection_log.add(item["id"])
                self.log.config(text=f"Auto-looted: {item['name']}")
            else:
                self.auto_loot_enabled = False
                self.log.config(text="Auto-Loot disabled (not enough coins).")
        self.update_ui()
        self.root.after(5000, self.auto_loot_tick)  # Repeat every 5s

    def roll_loot(self):
        if not self.first_roll_used:
            cost = 0
        else:
            cost = 15

        if self.coins < cost:
            self.log.config(text="❌ Not enough coins to roll loot! (Cost: 15)")
            return

        if cost > 0:
            self.coins -= cost
        self.first_roll_used = True

        # Create spin effect
        spin_win = Toplevel(self.root)
        spin_win.title("Rolling Loot...")
        spin_label = Label(spin_win, text="Rolling...", font=("Helvetica", 14))
        spin_label.pack(padx=20, pady=20)

        def spin(index=0):
            if index < 20:
                item = roll_loot_by_rarity()
                spin_label.config(text=item["name"], fg=RARITY_COLORS[item["rarity"]])
                spin_win.after(100, lambda: spin(index + 1))
            else:
                item = roll_loot_by_rarity()
                self.inventory.append(item)
                self.collection_log.add(item["id"])
                spin_label.config(text=f"🎉 {item['name']}!", fg=RARITY_COLORS[item["rarity"]])
                self.log.config(text=f"🎲 You rolled: {item['name']}!")
                self.update_ui()
                self.save_game()
                spin_win.after(1000, spin_win.destroy)

        spin()

    def sell_selected(self):
        selected = self.inventory_list.curselection()
        if not selected:
            return
        item = self.inventory[selected[0]]
        rarity = item["rarity"]
        coin_value = {
            "Common": 5,
            "Uncommon": 10,
            "Rare": 20,
            "Epic": 50,
            "Legendary": 100
        }.get(rarity, 0)

        self.coins += coin_value
        self.inventory.pop(selected[0])
        self.log.config(text=f"Sold {item['name']} for {coin_value} coins.")
        self.update_ui()
        self.save_game()

    def open_bulk_sell_menu(self):
        win = Toplevel(self.root)
        win.title("Bulk Sell")

        Label(win, text="Sell All Items By Rarity").pack(pady=5)

        for rarity in RARITY_ORDER:
            Button(
                win,
                text=f"Sell All {rarity} Items",
                fg=RARITY_COLORS[rarity],
                command=lambda r=rarity: self.bulk_sell(r, win)
            ).pack(padx=10, pady=2)

    def bulk_sell(self, rarity, window):
        coin_value = {
            "Common": 5,
            "Uncommon": 10,
            "Rare": 20,
            "Epic": 50,
            "Legendary": 100
        }.get(rarity, 0)

        items_to_sell = [item for item in self.inventory if item["rarity"] == rarity]
        count = len(items_to_sell)
        total_value = coin_value * count

        if count == 0:
            self.log.config(text=f"No {rarity} items to sell.")
            window.destroy()
            return

        # Confirm preview
        confirm = Toplevel(self.root)
        confirm.title("Confirm Bulk Sell")

        Label(confirm, text=f"Sell all {count} {rarity} items for {total_value} coins?").pack(padx=10, pady=10)

        def confirm_sell():
            self.inventory = [item for item in self.inventory if item["rarity"] != rarity]
            self.coins += total_value
            self.log.config(text=f"Sold {count} {rarity} items for {total_value} coins.")
            self.update_ui()
            self.save_game()
            confirm.destroy()
            window.destroy()

        Button(confirm, text="Confirm", command=confirm_sell).pack(side=LEFT, padx=20, pady=10)
        Button(confirm, text="Cancel", command=confirm.destroy).pack(side=RIGHT, padx=20, pady=10)



    def use_potion(self):
        if self.potions > 0 and self.hp < self.max_hp:
            self.hp = min(self.hp + 30, self.max_hp)
            self.potions -= 1
            self.log.config(text="🧪 You used a potion!")
        else:
            self.log.config(text="No potions or already full HP!")
        self.update_ui()
        self.save_game()

    def start_dungeon(self):
        if not self.equipped_weapon:
            self.log.config(text="Equip a weapon first!")
            return

        atk = self.equipped_weapon.get("atk", 0)
        defense = self.equipped_armor.get("def", 0) if self.equipped_armor else 0

        # Phase 1 - Regular enemies
        enemy_hp = 20 + self.level * 2
        self.log.config(text="Entering dungeon... Phase 1: Clearing mobs!")
        self.root.update()

        while enemy_hp > 0 and self.hp > 0:
            enemy_hp -= atk
            dmg = max(0, random.randint(5, 15) - defense)
            self.hp -= dmg

        if self.hp <= 0:
            self.hp = self.max_hp
            self.log.config(text="You were defeated by the dungeon mobs!")
            self.update_ui()
            self.save_game()
            return

        # Phase 2 - Boss Battle
        boss_hp = 40 + self.level * 3
        self.log.config(text="Phase 2: Boss Battle!")
        self.root.update()
        boss_name = random.choice(["Gravelord Xarn", "The Hollow Titan", "Crimson Wraith"])
        self.log.config(text=f"Boss Encountered: {boss_name}!")
        self.root.update()

        while boss_hp > 0 and self.hp > 0:
            boss_hp -= atk
            dmg = max(0, random.randint(10, 25) - defense)
            self.hp -= dmg

        if self.hp <= 0:
            self.hp = self.max_hp
            self.log.config(text=f"You were slain by {boss_name}!")
            self.update_ui()
            self.save_game()
            return

        # Victory rewards
        loot = roll_loot_by_rarity()
        bonus_loot = roll_loot_by_rarity()
        self.inventory.extend([loot, bonus_loot])
        self.collection_log.update([loot["id"], bonus_loot["id"]])
        self.coins += 10
        self.xp += 8

        self.log.config(text=f"Victory! Defeated {boss_name}.\nLooted: {loot['name']} and {bonus_loot['name']} (+20 coins, +15 XP)")
        if self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 2.0)

        self.update_ui()
        self.save_game()



    def refresh_shop_items(self):
        all_items = [
            {"name": "Potion", "cost": 10, "action": lambda: setattr(self, "potions", self.potions + 1)},
            {"name": "Auto-Loot I", "cost": 50, "action": lambda: setattr(self, "auto_loot", 1)},
            {"name": "Auto-Loot II", "cost": 150, "action": lambda: setattr(self, "auto_loot", 2)},
            {"name": "Auto-Loot III", "cost": 500, "action": lambda: setattr(self, "auto_loot", 3)},
            {"name": "XP Boost", "cost": 75, "action": lambda: setattr(self, "xp", self.xp + 25)},
            {"name": "Heal Scroll", "cost": 30, "action": lambda: setattr(self, "hp", min(self.hp + 50, self.max_hp))},
        ]
        self.shop_rotation = random.sample(all_items, k=3)
        self.last_shop_refresh = time.time()



    def open_shop(self):
        now = time.time()
        if now - self.last_shop_refresh > 300:  # 5 mins
            self.refresh_shop_items()

        win = Toplevel(self.root)
        win.title("Grimrick's Goods")

        Label(win, text=self.vendor_name, font=("Helvetica", 14, "bold"), fg="purple").pack()
        Label(win, text='"Ah, a fine day to part with your coins..."').pack(pady=(0, 10))

        def try_buy(item):
            if self.coins >= item["cost"]:
                self.coins -= item["cost"]
                item["action"]()
                self.log.config(text=f"💰 Bought {item['name']} for {item['cost']} coins!")
                self.update_ui()
                self.save_game()
            else:
                self.log.config(text=f"❌ Not enough coins for {item['name']}!")

        for item in self.shop_rotation:
            Button(win, text=f"{item['name']} ({item['cost']} coins)", width=30,
                command=lambda i=item: try_buy(i)).pack(pady=2)

        Button(win, text="🌀 Refresh Shop (Free every 5 min)", command=lambda: [self.refresh_shop_items(), win.destroy(), self.open_shop()]).pack(pady=5)



    def buy(self, what, cost):
        if self.coins < cost:
            self.log.config(text="Not enough coins!")
            return
        self.coins -= cost
        if what == "potion":
            self.potions += 1
            self.log.config(text="Bought 1 potion.")
        elif what == "loot":
            self.roll_loot()
        self.update_ui()
        self.save_game()

    def show_collection(self):
        win = Toplevel(self.root)
        win.title("Collection Log")
        total = len(LOOT_TABLE)
        unlocked = sum(1 for item in LOOT_TABLE if item["id"] in self.collection_log)
        percent = int(unlocked / total * 100)
        Label(win, text=f"Unlocked {unlocked}/{total} Items ({percent}%)", font=("Helvetica", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        sorted_items = sorted(LOOT_TABLE, key=lambda x: RARITY_ORDER.index(x["rarity"]))
        for rarity in RARITY_ORDER:
            group = [i for i in sorted_items if i["rarity"] == rarity]
            if not group:
                continue
            Label(win, text=f"{rarity} Items", fg=RARITY_COLORS[rarity], font=("Helvetica", 11, "bold")).pack(anchor="w", padx=10)
            for item in group:
                if item["id"] in self.collection_log:
                    text = f"{item['name']} - {item['desc']}"
                    color = RARITY_COLORS[item["rarity"]]
                else:
                    text = "??? - ???"
                    color = "gray"
                Label(win, text=text, fg=color).pack(anchor="w", padx=20)

    def save_game(self):
        os.makedirs("game_data", exist_ok=True)
        data = {
            "inventory": self.inventory,
            "collection_log": list(self.collection_log),
            "equipped_weapon": self.equipped_weapon,
            "equipped_armor": self.equipped_armor,
            "coins": self.coins,
            "xp": self.xp,
            "level": self.level,
            "xp_to_next": self.xp_to_next,
            "hp": self.hp,
            "potions": self.potions,
            "first_roll_used": self.first_roll_used,
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                self.inventory = data.get("inventory", [])
                self.collection_log = set(data.get("collection_log", []))
                self.equipped_weapon = data.get("equipped_weapon")
                self.equipped_armor = data.get("equipped_armor")
                self.coins = data.get("coins", 0)
                self.xp = data.get("xp", 0)
                self.level = data.get("level", 1)
                self.xp_to_next = data.get("xp_to_next", 20)
                self.hp = data.get("hp", 100)
                self.potions = data.get("potions", 0)
                self.first_roll_used = data.get("first_roll_used", False)


if __name__ == "__main__":
    root = Tk()
    game = Game(root)
    root.mainloop()

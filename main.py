import random

Cname = input("What is your name hero?    ")
print("Hello", Cname, "welcome to Tarramadura")

# Base stats (can be modified by class later)
CHP = 100
CSHP = 50
CMana = 200

def show_stats(hp, max_hp, mana, max_mana, shield, max_shield):
    hp_bar = "█ " * (hp // 10)
    mana_bar = "█ " * (mana // 20)
    shield_bar = "█ " * (shield // 10)

    print(f"HP:     {hp_bar} ({hp} / {max_hp})")
    print()
    print(f"Mana:   {mana_bar} ({mana} / {max_mana})")
    print()
    print(f"Shield: {shield_bar} ({shield} / {max_shield})")

def show_hp_bar(hp, max_hp):
    hp_bar = "█ " * (hp // 10)
    print(f"HP:     {hp_bar} ({hp} / {max_hp})")

def show_mana_bar(mana, max_mana):
    mana_bar = "█ " * (mana // 20)
    print(f"Mana:   {mana_bar} ({mana} / {max_mana})")

def show_shield_bar(shield, max_shield):
    shield_bar = "█ " * (shield // 10)
    print(f"Shield: {shield_bar} ({shield} / {max_shield})")

def clamp_hp(hp):
    return max(0, hp)

def enemy_attack(player_hp, player_shield, is_defending, base_damage, enemy_name):
    if is_defending:
        damage = base_damage // 2
        print(f"\nThe {enemy_name} attacks! You are defending, so damage is halved: {base_damage} -> {damage}.")
    else:
        damage = base_damage
        print(f"\nThe {enemy_name} attacks! It deals {damage} damage.")

    if player_shield > 0:
        if player_shield >= damage:
            player_shield -= damage
            print(f"Your shield absorbed the hit! Shield is now {player_shield}.")
        else:
            leftover = damage - player_shield
            player_shield = 0
            player_hp -= leftover
            player_hp = clamp_hp(player_hp)
            print("Your shield broke!")
            if player_hp <= 0:
                print("You have been defeated...")
    else:
        player_hp -= damage
        player_hp = clamp_hp(player_hp)
        if player_hp <= 0:
            print("You have been defeated...")

    return player_hp, player_shield

answer = input("Welcome to the Tutorial! Would you like to begin? (yes/no): ")

if answer.lower() in ("yes", "y"):
    choice_text = "yes"
    print("You chose:", choice_text)
    print("Starting the tutorial...")
    print("You have a set amount of HP, Shield HP, and Mana. If you lose all your HP you die, and some attacks require Mana. If you run out of Mana you have to wait for it to regenerate.")

    show_stats(CHP, 100, CMana, 200, CSHP, 50)

    defending = False
  
    def strike(target_hp):
        damage = 10
        print(f"\nYou used Strike! It dealt {damage} damage.")
        target_hp -= damage
        target_hp = clamp_hp(target_hp)
        print(f"Enemy now has {target_hp} HP.")
        return target_hp
    
    def heavy_blow(target_hp, current_mana):
        damage = 30
        mana_cost = 5
        if current_mana < mana_cost:
            print("\nNot enough Mana for Heavy Blow!")
            return target_hp, current_mana
        print(f"\nYou used Heavy Blow! It dealt {damage} damage.")
        target_hp -= damage
        target_hp = clamp_hp(target_hp)
        current_mana -= mana_cost
        print(f"Enemy now has {target_hp} HP.")
        print(f"You have {current_mana} Mana left.")
        return target_hp, current_mana

    enemy_name = "Tarrogoblin"
    enemy_max_hp = 30
    enemy_hp = enemy_max_hp

    print(f"\nA wild {enemy_name} appears! It has {enemy_hp} HP.")
    xp_reward = enemy_max_hp // 10
    tutorial_completed = False

    while enemy_hp > 0 and CHP > 0:
        action = input("\nType 'Strike', 'HB', 'Defend', or 'Escape': ")

        if action.lower() == "escape":
            print("You escaped the tutorial.")
            break

        elif action.lower() == "strike":
            enemy_hp = strike(enemy_hp)
            defending = False
            print("\n--- Status after Strike ---")
            show_hp_bar(CHP, 100)
            print(f"Enemy HP: {enemy_hp} / {enemy_max_hp}\n")

        elif action.lower() in ("heavy_blow", "hb"):
            old_mana = CMana
            enemy_hp, CMana = heavy_blow(enemy_hp, CMana)
            defending = False
            if CMana != old_mana:
                print("\n--- Status after Heavy Blow ---")
                show_mana_bar(CMana, 200)
                print(f"Enemy HP: {enemy_hp} / {enemy_max_hp}\n")

        elif action.lower() == "defend":
            print("\nYou raise your guard. The next enemy attack will do half damage.")
            defending = True

        else:
            print("Invalid command. Type 'Strike', 'HB', 'Defend', or 'Escape'.")
            continue

        if enemy_hp <= 0:
            enemy_hp = 0
            print(f"\nYou defeated the {enemy_name}!")
            print(f"You earned {xp_reward} XP!")
            print("Tutorial completed!")
            tutorial_completed = True
            break

        CHP, CSHP = enemy_attack(CHP, CSHP, defending, 5, enemy_name)
        defending = False

        if CHP > 0:
            print("\n--- Status after Tarrogoblin attack ---")
            show_hp_bar(CHP, 100)
            print()
            show_shield_bar(CSHP, 50)
            print()
            print(f"Enemy HP: {enemy_hp} / {enemy_max_hp}\n")

    if CHP <= 0:
        print("\nGame Over. Better luck next time!")
    elif enemy_hp <= 0:
        pass

    # ----- CLASS SELECTION (after tutorial) -----
    if tutorial_completed:
        print("\n=== Class Selection ===")
        print("You have completed the tutorial!")
        print("Now you must choose your path:")
        print("- Mage: High Mana, powerful magic attacks")
        print("- Swordsman: Balanced stats, strong physical attacks")

        while True:
            class_choice = input("\nDo you want to be a Mage or a Swordsman? (Mage/Swordsman): ")

            if class_choice.lower() == "mage":
                player_class = "Mage"
                CMana = 250
                print("\nYou have chosen the path of the Mage!")
                print("You gain the spells: Fireball (40 dmg, 20 mana) and Shock (20 dmg, 40 mana, may paralyse).")
                break
            elif class_choice.lower() == "swordsman":
                player_class = "Swordsman"
                CHP = 120
                print("\nYou have chosen the path of the Swordsman!")
                print("You gain the attacks: Slash (20 dmg, 0 mana) and Sword Duality (doubles your exclusive attacks).")
                break
            elif class_choice.lower() == "shrimp":  # Hidden Easter egg - type "shrimp"
                player_class = "Shrimp"
                CHP = 175
                CMana = 300  # Give Shrimp good mana for water spells
                print("\n???")
                print("A mysterious voice whispers: 'You have chosen... the way of the Shrimp.'")
                print("You feel small but powerful. The ocean's power flows through you.")
                print("You gain the spells: Tsunami (35 dmg, 10 mana), Whirlpool (50 dmg, 40 mana, may trap), Riptide (25 dmg, 25 mana).")
                break
            else:
                print("Invalid choice. Please type 'Mage' or 'Swordsman'.")

        print(f"\nWelcome, {player_class} {Cname}! Your adventure in Tarramadura continues...")

        # ----- POST-CLASS BATTLE SETUP -----
        enemy_name = "Bandit"
        enemy_max_hp = 60
        enemy_hp = enemy_max_hp
        print(f"\nA wild {enemy_name} appears! It has {enemy_hp} HP.")

        enemy_paralysed_turns = 0
        enemy_trapped_turns = 0  # For Shrimp's Whirlpool
        sword_duality_active = False

        # ----- MAIN BATTLE LOOP (vs Bandit) -----
        while enemy_hp > 0 and CHP > 0:

            if enemy_paralysed_turns > 0:
                print(f"\nThe {enemy_name} is paralysed and cannot act this turn ({enemy_paralysed_turns} turn(s) left).")
                enemy_paralysed_turns -= 1
                enemy_will_attack = False
            elif enemy_trapped_turns > 0:
                print(f"\nThe {enemy_name} is trapped in a whirlpool and cannot act this turn ({enemy_trapped_turns} turn(s) left).")
                enemy_trapped_turns -= 1
                enemy_will_attack = False
            else:
                enemy_will_attack = True

            # ----- PLAYER TURN -----
            if player_class == "Swordsman":
                action = input("\nType 'Slash', 'Sword Duality', 'Defend', or 'Escape': ")

                if action.lower() == "escape":
                    print("You escaped the battle.")
                    break

                elif action.lower() == "slash":
                    damage = 20
                    if sword_duality_active:
                        damage *= 2
                        print(f"\nYou used Slash with Sword Duality! It dealt {damage} damage.")
                        sword_duality_active = False
                    else:
                        print(f"\nYou used Slash! It dealt {damage} damage.")

                    enemy_hp -= damage
                    enemy_hp = clamp_hp(enemy_hp)
                    print(f"Enemy now has {enemy_hp} HP.")

                elif action.lower() in ("sword duality", "duality"):
                    sword_duality_active = True
                    print("\nYou activate Sword Duality! Your next Swordsman-exclusive attack will deal double damage.")

                elif action.lower() == "defend":
                    print("\nYou raise your guard. The next enemy attack will do half damage.")
                    defending = True

                else:
                    print("Invalid command. Type 'Slash', 'Sword Duality', 'Defend', or 'Escape'.")
                    continue

            elif player_class == "Mage":
                action = input("\nType 'Fireball', 'Shock', 'Defend', or 'Escape': ")

                if action.lower() == "escape":
                    print("You escaped the battle.")
                    break

                elif action.lower() == "fireball":
                    mana_cost = 20
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Fireball!")
                        continue
                    damage = 40
                    CMana -= mana_cost
                    print(f"\nYou cast Fireball! It dealt {damage} damage.")
                    enemy_hp -= damage
                    enemy_hp = clamp_hp(enemy_hp)
                    print(f"Enemy now has {enemy_hp} HP.")

                elif action.lower() == "shock":
                    mana_cost = 40
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Shock!")
                        continue
                    damage = 20
                    CMana -= mana_cost
                    print(f"\nYou cast Shock! It dealt {damage} damage.")

                    if random.random() < 0.75:
                        enemy_paralysed_turns = 2
                        print("The enemy is paralysed and cannot act for 2 turns!")
                    else:
                        print("The enemy resisted the paralysis.")

                    enemy_hp -= damage
                    enemy_hp = clamp_hp(enemy_hp)
                    print(f"Enemy now has {enemy_hp} HP.")

                elif action.lower() == "defend":
                    print("\nYou raise your guard. The next enemy attack will do half damage.")
                    defending = True

                else:
                    print("Invalid command. Type 'Fireball', 'Shock', 'Defend', or 'Escape'.")
                    continue

            elif player_class == "Shrimp":
                action = input("\nType 'Tsunami', 'Whirlpool', 'Riptide', 'Defend', or 'Escape': ")

                if action.lower() == "escape":
                    print("You swam away from the battle.")
                    break

                elif action.lower() == "tsunami":
                    mana_cost = 10
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Tsunami!")
                        continue
                    damage = 35
                    CMana -= mana_cost
                    print(f"\nYou used Tsunami! It dealt {damage} damage.")
                    enemy_hp -= damage
                    enemy_hp = clamp_hp(enemy_hp)
                    print(f"Enemy now has {enemy_hp} HP.")

                elif action.lower() == "whirlpool":
                    mana_cost = 40
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Whirlpool!")
                        continue
                    damage = 50
                    CMana -= mana_cost
                    print(f"\nYou cast Whirlpool! It dealt {damage} damage.")

                    if random.random() < 0.75:
                        enemy_trapped_turns = 2
                        print("The enemy is trapped in the whirlpool and cannot act for 2 turns!")
                    else:
                        print("The enemy was too tough for the whirlpool.")

                    enemy_hp -= damage
                    enemy_hp = clamp_hp(enemy_hp)
                    print(f"Enemy now has {enemy_hp} HP.")

                elif action.lower() == "riptide":
                    mana_cost = 25
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Riptide!")
                        continue
                    damage = 25
                    CMana -= mana_cost
                    print(f"\nYou used Riptide! It dealt {damage} damage.")
                    enemy_hp -= damage
                    enemy_hp = clamp_hp(enemy_hp)
                    print(f"Enemy now has {enemy_hp} HP.")

                elif action.lower() == "defend":
                    print("\nYou raise your shrimpy tail. The next enemy attack will do half damage.")
                    defending = True

                else:
                    print("Invalid command. Type 'Tsunami', 'Whirlpool', 'Riptide', 'Defend', or 'Escape'.")
                    continue

            else:
                print("Unknown class. Ending battle.")
                break

            if enemy_hp <= 0:
                enemy_hp = 0
                print(f"\nYou defeated the {enemy_name}!")
                break

            # ----- ENEMY TURN -----
            if enemy_will_attack:
                CHP, CSHP = enemy_attack(CHP, CSHP, defending, 5, enemy_name)
                defending = False

                if CHP > 0:
                    print("\n--- Status after enemy attack ---")
                    show_hp_bar(CHP, 100)
                    print()
                    show_shield_bar(CSHP, 50)
                    print()
                    print(f"Enemy HP: {enemy_hp} / {enemy_max_hp}\n")
            else:
                defending = False
                print("\n--- Status ---")
                show_hp_bar(CHP, 100)
                print()
                show_shield_bar(CSHP, 50)
                print()
                print(f"Enemy HP: {enemy_hp} / {enemy_max_hp}\n")

        if CHP <= 0:
            print("\nGame Over. Better luck next time!")
        elif enemy_hp <= 0:
            print("\nVictory! Your journey as a", player_class, "continues...")

    # ----- WOODLAND PATH -----
    if tutorial_completed and CHP > 0:
        print("\n=== The Woodland Path ===")
        print("You step onto a dark, twisting path through the woods...")
        print("Two Tarrogoblins leap out to attack you!")

        goblin1_name = "Tarrogoblin"
        goblin1_max_hp = 30
        goblin1_hp = goblin1_max_hp
        goblin1_damage = 5

        goblin2_name = "Empowered Tarrogoblin"
        goblin2_max_hp = 50
        goblin2_hp = goblin2_max_hp
        goblin2_damage = 30

        print(f"\nA wild {goblin1_name} ({goblin1_hp} HP) and {goblin2_name} ({goblin2_hp} HP) appear!")

        enemy_paralysed_turns = 0
        enemy_trapped_turns = 0
        sword_duality_active = False

        while (goblin1_hp > 0 or goblin2_hp > 0) and CHP > 0:

            if goblin1_hp > 0 and goblin2_hp > 0:
                print(f"\nEnemies: {goblin1_name} HP: {goblin1_hp}/{goblin1_max_hp}, {goblin2_name} HP: {goblin2_hp}/{goblin2_max_hp}")
            elif goblin1_hp > 0:
                print(f"\nEnemy: {goblin1_name} HP: {goblin1_hp}/{goblin1_max_hp}")
            elif goblin2_hp > 0:
                print(f"\nEnemy: {goblin2_name} HP: {goblin2_hp}/{goblin2_max_hp}")

            if enemy_paralysed_turns > 0 or enemy_trapped_turns > 0:
                if enemy_paralysed_turns > 0:
                    print(f"\nBoth Tarrogoblins are paralysed and cannot act this turn ({enemy_paralysed_turns} turn(s) left).")
                    enemy_paralysed_turns -= 1
                if enemy_trapped_turns > 0:
                    print(f"\nBoth Tarrogoblins are trapped and cannot act this turn ({enemy_trapped_turns} turn(s) left).")
                    enemy_trapped_turns -= 1
                enemies_will_attack = False
            else:
                enemies_will_attack = True

            # ----- PLAYER TURN -----
            if player_class == "Swordsman":
                action = input("\nType 'Slash', 'Sword Duality', 'Defend', or 'Escape': ")

                if action.lower() == "escape":
                    print("You fled the Woodland Path.")
                    break

                elif action.lower() == "slash":
                    damage = 20
                    if sword_duality_active:
                        damage *= 2
                        print(f"\nYou used Slash with Sword Duality! It dealt {damage} damage.")
                        sword_duality_active = False
                    else:
                        print(f"\nYou used Slash! It dealt {damage} damage.")

                    if goblin1_hp > 0 and goblin2_hp > 0:
                        target = input("Choose target: 1 for Tarrogoblin, 2 for Empowered Tarrogoblin: ")
                        if target == "1":
                            goblin1_hp -= damage
                            goblin1_hp = clamp_hp(goblin1_hp)
                        elif target == "2":
                            goblin2_hp -= damage
                            goblin2_hp = clamp_hp(goblin2_hp)
                        else:
                            print("Invalid target, attack fails.")
                            continue
                    elif goblin1_hp > 0:
                        goblin1_hp -= damage
                        goblin1_hp = clamp_hp(goblin1_hp)
                    elif goblin2_hp > 0:
                        goblin2_hp -= damage
                        goblin2_hp = clamp_hp(goblin2_hp)

                elif action.lower() in ("sword duality", "duality"):
                    sword_duality_active = True
                    print("\nYou activate Sword Duality! Your next Swordsman-exclusive attack will deal double damage.")

                elif action.lower() == "defend":
                    print("\nYou raise your guard. The next enemy attacks will do half damage.")
                    defending = True

                else:
                    print("Invalid command. Type 'Slash', 'Sword Duality', 'Defend', or 'Escape'.")
                    continue

            elif player_class == "Mage":
                action = input("\nType 'Fireball', 'Shock', 'Defend', or 'Escape': ")

                if action.lower() == "escape":
                    print("You fled the Woodland Path.")
                    break

                elif action.lower() == "fireball":
                    mana_cost = 20
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Fireball!")
                        continue
                    damage = 40
                    CMana -= mana_cost
                    print(f"\nYou cast Fireball! It dealt {damage} damage.")

                    if goblin1_hp > 0 and goblin2_hp > 0:
                        target = input("Choose target: 1 for Tarrogoblin, 2 for Empowered Tarrogoblin: ")
                        if target == "1":
                            goblin1_hp -= damage
                            goblin1_hp = clamp_hp(goblin1_hp)
                        elif target == "2":
                            goblin2_hp -= damage
                            goblin2_hp = clamp_hp(goblin2_hp)
                        else:
                            print("Invalid target, attack fails.")
                            continue
                    elif goblin1_hp > 0:
                        goblin1_hp -= damage
                        goblin1_hp = clamp_hp(goblin1_hp)
                    elif goblin2_hp > 0:
                        goblin2_hp -= damage
                        goblin2_hp = clamp_hp(goblin2_hp)

                elif action.lower() == "shock":
                    mana_cost = 40
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Shock!")
                        continue
                    damage = 20
                    CMana -= mana_cost
                    print(f"\nYou cast Shock! It dealt {damage} damage.")

                    if random.random() < 0.75:
                        enemy_paralysed_turns = 2
                        print("The Tarrogoblins are paralysed and cannot act for 2 turns!")
                    else:
                        print("The Tarrogoblins resisted the paralysis.")

                    if goblin1_hp > 0 and goblin2_hp > 0:
                        target = input("Choose target: 1 for Tarrogoblin, 2 for Empowered Tarrogoblin: ")
                        if target == "1":
                            goblin1_hp -= damage
                            goblin1_hp = clamp_hp(goblin1_hp)
                        elif target == "2":
                            goblin2_hp -= damage
                            goblin2_hp = clamp_hp(goblin2_hp)
                        else:
                            print("Invalid target, attack fails.")
                            continue
                    elif goblin1_hp > 0:
                        goblin1_hp -= damage
                        goblin1_hp = clamp_hp(goblin1_hp)
                    elif goblin2_hp > 0:
                        goblin2_hp -= damage
                        goblin2_hp = clamp_hp(goblin2_hp)

                elif action.lower() == "defend":
                    print("\nYou raise your guard. The next enemy attacks will do half damage.")
                    defending = True

                else:
                    print("Invalid command. Type 'Fireball', 'Shock', 'Defend', or 'Escape'.")
                    continue

            elif player_class == "Shrimp":
                action = input("\nType 'Tsunami', 'Whirlpool', 'Riptide', 'Defend', or 'Escape': ")

                if action.lower() == "escape":
                    print("You fled the Woodland Path.")
                    break

                elif action.lower() == "tsunami":
                    mana_cost = 10
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Tsunami!")
                        continue
                    damage = 35
                    CMana -= mana_cost
                    print(f"\nYou used Tsunami! It dealt {damage} damage.")

                    if goblin1_hp > 0 and goblin2_hp > 0:
                        target = input("Choose target: 1 for Tarrogoblin, 2 for Empowered Tarrogoblin: ")
                        if target == "1":
                            goblin1_hp -= damage
                            goblin1_hp = clamp_hp(goblin1_hp)
                        elif target == "2":
                            goblin2_hp -= damage
                            goblin2_hp = clamp_hp(goblin2_hp)
                        else:
                            print("Invalid target, attack fails.")
                            continue
                    elif goblin1_hp > 0:
                        goblin1_hp -= damage
                        goblin1_hp = clamp_hp(goblin1_hp)
                    elif goblin2_hp > 0:
                        goblin2_hp -= damage
                        goblin2_hp = clamp_hp(goblin2_hp)

                elif action.lower() == "whirlpool":
                    mana_cost = 40
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Whirlpool!")
                        continue
                    damage = 50
                    CMana -= mana_cost
                    print(f"\nYou cast Whirlpool! It dealt {damage} damage.")

                    if random.random() < 0.75:
                        enemy_trapped_turns = 2
                        print("The Tarrogoblins are trapped in the whirlpool and cannot act for 2 turns!")
                    else:
                        print("The Tarrogoblins were too tough for the whirlpool.")

                    if goblin1_hp > 0 and goblin2_hp > 0:
                        target = input("Choose target: 1 for Tarrogoblin, 2 for Empowered Tarrogoblin: ")
                        if target == "1":
                            goblin1_hp -= damage
                            goblin1_hp = clamp_hp(goblin1_hp)
                        elif target == "2":
                            goblin2_hp -= damage
                            goblin2_hp = clamp_hp(goblin2_hp)
                        else:
                            print("Invalid target, attack fails.")
                            continue
                    elif goblin1_hp > 0:
                        goblin1_hp -= damage
                        goblin1_hp = clamp_hp(goblin1_hp)
                    elif goblin2_hp > 0:
                        goblin2_hp -= damage
                        goblin2_hp = clamp_hp(goblin2_hp)

                elif action.lower() == "riptide":
                    mana_cost = 25
                    if CMana < mana_cost:
                        print("\nNot enough Mana for Riptide!")
                        continue
                    damage = 25
                    CMana -= mana_cost
                    print(f"\nYou used Riptide! It dealt {damage} damage.")

                    if goblin1_hp > 0 and goblin2_hp > 0:
                        target = input("Choose target: 1 for Tarrogoblin, 2 for Empowered Tarrogoblin: ")
                        if target == "1":
                            goblin1_hp -= damage
                            goblin1_hp = clamp_hp(goblin1_hp)
                        elif target == "2":
                            goblin2_hp -= damage
                            goblin2_hp = clamp_hp(goblin2_hp)
                        else:
                            print("Invalid target, attack fails.")
                            continue
                    elif goblin1_hp > 0:
                        goblin1_hp -= damage
                        goblin1_hp = clamp_hp(goblin1_hp)
                    elif goblin2_hp > 0:
                        goblin2_hp -= damage
                        goblin2_hp = clamp_hp(goblin2_hp)

                elif action.lower() == "defend":
                    print("\nYou raise your shrimpy tail. The next enemy attacks will do half damage.")
                    defending = True

                else:
                    print("Invalid command. Type 'Tsunami', 'Whirlpool', 'Riptide', 'Defend', or 'Escape'.")
                    continue

            if goblin1_hp <= 0 and goblin2_hp <= 0:
                print("\nYou defeated both Tarrogoblins!")
                break

            if enemies_will_attack:
                if goblin1_hp > 0:
                    CHP, CSHP = enemy_attack(CHP, CSHP, defending, goblin1_damage, goblin1_name)
                if goblin2_hp > 0:
                    CHP, CSHP = enemy_attack(CHP, CSHP, defending, goblin2_damage, goblin2_name)

                defending = False

                if CHP > 0:
                    print("\n--- Status after Tarrogoblin attacks ---")
                    show_hp_bar(CHP, 100)
                    print()
                    show_shield_bar(CSHP, 50)
                    print()
                    if goblin1_hp > 0 and goblin2_hp > 0:
                        print(f"{goblin1_name} HP: {goblin1_hp}/{goblin1_max_hp}, {goblin2_name} HP: {goblin2_hp}/{goblin2_max_hp}\n")
                    elif goblin1_hp > 0:
                        print(f"{goblin1_name} HP: {goblin1_hp}/{goblin1_max_hp}\n")
                    elif goblin2_hp > 0:
                        print(f"{goblin2_name} HP: {goblin2_hp}/{goblin2_max_hp}\n")
            else:
                defending = False
                print("\n--- Status ---")
                show_hp_bar(CHP, 100)
                print()
                show_shield_bar(CSHP, 50)
                print()
                if goblin1_hp > 0 and goblin2_hp > 0:
                    print(f"{goblin1_name} HP: {goblin1_hp}/{goblin1_max_hp}, {goblin2_name} HP: {goblin2_hp}/{goblin2_max_hp}\n")
                elif goblin1_hp > 0:
                    print(f"{goblin1_name} HP: {goblin1_hp}/{goblin1_max_hp}\n")
                elif goblin2_hp > 0:
                    print(f"{goblin2_name} HP: {goblin2_hp}/{goblin2_max_hp}\n")

            if CHP <= 0:
                break

        if CHP <= 0:
            print("\nGame Over. The Woodland Path claims another hero...")
        elif goblin1_hp <= 0 and goblin2_hp <= 0:
            print("\nYou catch your breath... but something stronger approaches.")
            print("A towering figure emerges from the shadows...")

            # ----- TARROGOBLIN WARRIOR BOSS -----
            warrior_name = "Tarrogoblin Warrior"
            warrior_max_hp = 80
            warrior_hp = warrior_max_hp

            weapon_choice = random.choice(["Staff", "Cursed Blade"])
            if weapon_choice == "Staff":
                warrior_damage = 25
                print(f"The {warrior_name} raises a glowing {weapon_choice}! (Damage: {warrior_damage})")
            else:
                warrior_damage = 35
                print(f"The {warrior_name} draws a {weapon_choice}! (Damage: {warrior_damage})")

            print(f"\nThe {warrior_name} challenges you! It has {warrior_hp} HP.")
            enemy_paralysed_turns = 0
            enemy_trapped_turns = 0
            sword_duality_active = False

            while warrior_hp > 0 and CHP > 0:

                if enemy_paralysed_turns > 0:
                    print(f"\nThe {warrior_name} is paralysed and cannot act this turn ({enemy_paralysed_turns} turn(s) left).")
                    enemy_paralysed_turns -= 1
                    warrior_will_attack = False
                elif enemy_trapped_turns > 0:
                    print(f"\nThe {warrior_name} is trapped and cannot act this turn ({enemy_trapped_turns} turn(s) left).")
                    enemy_trapped_turns -= 1
                    warrior_will_attack = False
                else:
                    warrior_will_attack = True

                # ----- PLAYER TURN -----
                if player_class == "Swordsman":
                    action = input("\nType 'Slash', 'Sword Duality', 'Defend', or 'Escape': ")

                    if action.lower() == "escape":
                        print("You fled from the Tarrogoblin Warrior.")
                        break

                    elif action.lower() == "slash":
                        damage = 20
                        if sword_duality_active:
                            damage *= 2
                            print(f"\nYou used Slash with Sword Duality! It dealt {damage} damage.")
                            sword_duality_active = False
                        else:
                            print(f"\nYou used Slash! It dealt {damage} damage.")

                        warrior_hp -= damage
                        warrior_hp = clamp_hp(warrior_hp)
                        print(f"{warrior_name} now has {warrior_hp} HP.")

                    elif action.lower() in ("sword duality", "duality"):
                        sword_duality_active = True
                        print("\nYou activate Sword Duality! Your next Swordsman-exclusive attack will deal double damage.")

                    elif action.lower() == "defend":
                        print("\nYou raise your guard. The next enemy attack will do half damage.")
                        defending = True

                    else:
                        print("Invalid command. Type 'Slash', 'Sword Duality', 'Defend', or 'Escape'.")
                        continue

                elif player_class == "Mage":
                    action = input("\nType 'Fireball', 'Shock', 'Defend', or 'Escape': ")

                    if action.lower() == "escape":
                        print("You fled from the Tarrogoblin Warrior.")
                        break

                    elif action.lower() == "fireball":
                        mana_cost = 20
                        if CMana < mana_cost:
                            print("\nNot enough Mana for Fireball!")
                            continue
                        damage = 40
                        CMana -= mana_cost
                        print(f"\nYou cast Fireball! It dealt {damage} damage.")
                        warrior_hp -= damage
                        warrior_hp = clamp_hp(warrior_hp)
                        print(f"{warrior_name} now has {warrior_hp} HP.")

                    elif action.lower() == "shock":
                        mana_cost = 40
                        if CMana < mana_cost:
                            print("\nNot enough Mana for Shock!")
                            continue
                        damage = 20
                        CMana -= mana_cost
                        print(f"\nYou cast Shock! It dealt {damage} damage.")

                        if random.random() < 0.75:
                            enemy_paralysed_turns = 2
                            print(f"The {warrior_name} is paralysed and cannot act for 2 turns!")
                        else:
                            print(f"The {warrior_name} resisted the paralysis.")

                        warrior_hp -= damage
                        warrior_hp = clamp_hp(warrior_hp)
                        print(f"{warrior_name} now has {warrior_hp} HP.")

                    elif action.lower() == "defend":
                        print("\nYou raise your guard. The next enemy attack will do half damage.")
                        defending = True

                    else:
                        print("Invalid command. Type 'Fireball', 'Shock', 'Defend', or 'Escape'.")
                        continue

                elif player_class == "Shrimp":
                    action = input("\nType 'Tsunami', 'Whirlpool', 'Riptide', 'Defend', or 'Escape': ")

                    if action.lower() == "escape":
                        print("You swam from the Tarrogoblin Warrior.")
                        break

                    elif action.lower() == "tsunami":
                        mana_cost = 10
                        if CMana < mana_cost:
                            print("\nNot enough Mana for Tsunami!")
                            continue
                        damage = 35
                        CMana -= mana_cost
                        print(f"\nYou used Tsunami! It dealt {damage} damage.")
                        warrior_hp -= damage
                        warrior_hp = clamp_hp(warrior_hp)
                        print(f"{warrior_name} now has {warrior_hp} HP.")

                    elif action.lower() == "whirlpool":
                        mana_cost = 40
                        if CMana < mana_cost:
                            print("\nNot enough Mana for Whirlpool!")
                            continue
                        damage = 50
                        CMana -= mana_cost
                        print(f"\nYou cast Whirlpool! It dealt {damage} damage.")

                        if random.random() < 0.75:
                            enemy_trapped_turns = 2
                            print(f"The {warrior_name} is trapped in the whirlpool and cannot act for 2 turns!")
                        else:
                            print(f"The {warrior_name} was too tough for the whirlpool.")

                        warrior_hp -= damage
                        warrior_hp = clamp_hp(warrior_hp)
                        print(f"{warrior_name} now has {warrior_hp} HP.")

                    elif action.lower() == "riptide":
                        mana_cost = 25
                        if CMana < mana_cost:
                            print("\nNot enough Mana for Riptide!")
                            continue
                        damage = 25
                        CMana -= mana_cost
                        print(f"\nYou used Riptide! It dealt {damage} damage.")
                        warrior_hp -= damage
                        warrior_hp = clamp_hp(warrior_hp)
                        print(f"{warrior_name} now has {warrior_hp} HP.")

                    elif action.lower() == "defend":
                        print("\nYou raise your shrimpy tail. The next enemy attack will do half damage.")
                        defending = True

                    else:
                        print("Invalid command. Type 'Tsunami', 'Whirlpool', 'Riptide', 'Defend', or 'Escape'.")
                        continue

                if warrior_hp <= 0:
                    print(f"\nYou defeated the {warrior_name}!")
                    print("The Woodland Path is cleared... for now.")
                    break

                if warrior_will_attack:
                    CHP, CSHP = enemy_attack(CHP, CSHP, defending, warrior_damage, warrior_name)
                    defending = False

                    if CHP > 0:
                        print("\n--- Status after Warrior attack ---")
                        show_hp_bar(CHP, 100)
                        print()
                        show_shield_bar(CSHP, 50)
                        print()
                        print(f"{warrior_name} HP: {warrior_hp}/{warrior_max_hp}\n")
                else:
                    defending = False
                    print("\n--- Status ---")
                    show_hp_bar(CHP, 100)
                    print()
                    show_shield_bar(CSHP, 50)
                    print()
                    print(f"{warrior_name} HP: {warrior_hp}/{warrior_max_hp}\n")

            if CHP <= 0:
                print("\nGame Over. The Tarrogoblin Warrior has bested you.")
            elif warrior_hp <= 0:
                print("\nYou stand victorious over the Woodland Path.")
                print("Your legend in Tarramadura grows...")

else:
    choice_text = "no"
    print("You chose:", choice_text)
    print("Okay, skipping the tutorial.")
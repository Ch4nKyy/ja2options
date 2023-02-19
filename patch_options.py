from configupdater import ConfigUpdater, Option
import argparse
import shutil
import time


def upsert(updater: ConfigUpdater, section: str, key: str, value: str):
    try:
        updater[section][key].value = value
    except KeyError:
        if not updater.has_section(section):
            updater.add_section(section)
            updater.get_section(section).add_before.space()
        o = Option(key, value)
        updater.get_section(section).add_option(o)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This tool patches a Ja2_Options.INI so that my favourite settings are used, '
        'but mod specific values arent removed.')
    parser.add_argument('filepath', type=str, help='')
    args = parser.parse_args()

    updater = ConfigUpdater()
    updater.read(args.filepath)

    # Macht den Anfang bzw das ganze Game sauschwer.
    # Und man muss an ewig langen Fights mit Militia teilnehmen.
    upsert(updater, "Strategic Event Settings", "TRIGGER_MASSIVE_ENEMY_COUNTERATTACK_AT_DRASSEN", "FALSE")
    upsert(updater, "Strategic Event Settings", "AGGRESSIVE_STRATEGIC_AI", "0")

    # Erfordert sonst, dass man immer einen Merc mit dem Com Talent hat,
    # um feindliche Unterstuetzung abzuwehren.
    upsert(updater, "Strategic Gameplay Settings", "ALLOW_REINFORCEMENTS", "FALSE")

    # Nervt.
    upsert(updater, "Recruitment Settings", "MERCS_CAN_DIE_ON_ASSIGNMENT", "FALSE")
    upsert(updater, "Recruitment Settings", "MERCS_CAN_BE_ON_ASSIGNMENT", "2")

    # Nervt, weil der Loadscreen dann laenger bleibt.
    upsert(updater, "Graphics Settings", "USE_LOADSCREENHINTS", "FALSE")

    # Die sind doch eh alle kacke, also gib sie uns von Anfang an.
    upsert(updater, "Recruitment Settings", "MERC_WEBSITE_IMMEDIATELY_AVAILABLE", "TRUE")

    # In Vanilla kriegt man sie erst nach 3/4/5 Staedten. Da sind sie unnoetig!
    # Mit dem Setting kriegt man sie nach 1/2/3.
    upsert(updater, "Recruitment Settings", "EARLY_REBELS_RECRUITMENT", "2")

    # Why not.
    upsert(updater, "Recruitment Settings", "RECRUITABLE_JOHN_KULBA", "TRUE")
    upsert(updater, "Recruitment Settings", "RECRUITABLE_JOHN_KULBA_DELAY", "7")

    # Praktisch.
    upsert(updater, "Recruitment Settings", "SHOW_SKILLS_IN_HIRING_PAGE", "TRUE")

    # Ich mag die Gear Auswahl!
    upsert(updater, "Graphics Settings", "USE_NEW_STARTING_GEAR_INTERFACE", "TRUE")

    # Nervt.
    upsert(updater, "Tactical Interface Settings", "HIDE_BULLET_COUNT_INTENSITY", "0")

    # Erfordert sonst, dass man immer einen Merc mit dem Scouting Talent hat.
    upsert(updater, "Tactical Difficulty Settings", "ENABLE_CHANCE_OF_ENEMY_AMBUSHES", "FALSE")
    upsert(updater, "Strategic Gameplay Settings", "NO_ENEMY_DETECTION_WITHOUT_RECON", "FALSE")

    # Nervt.
    upsert(updater, "Bobby Ray Settings", "STEALING_FROM_SHIPMENTS_DISABLED", "TRUE")
    upsert(updater, "Bobby Ray Settings", "CHANCE_OF_SHIPMENT_LOSS", "0")

    # Horde-Modus… find ich iwie unpassend.
    upsert(updater, "Strategic Enemy AI Settings", "NEW_AGGRESSIVE_AI", "FALSE")

    # Just let me conquer one sector after another and heal up in between.
    # It is still possible that enemies come to me!
    upsert(updater, "Strategic Enemy AI Settings", "ENEMY_INVESTIGATE_SECTOR", "FALSE")

    # Nervt, dauert doch eh schon laenger mit schlechter Leadership!
    upsert(updater, "Militia Training Settings", "LEADERSHIP_AFFECTS_MILITIA_QUANTITY", "FALSE")
    upsert(updater, "Militia Training Settings", "MINIMUM_LEADERSHIP_TO_TRAIN_MILITIA", "0")

    # Arulco Revisited und Vengeance Reloaded haben doppelt so grosse Staedte,
    # ich will aber nicht doppelt so lange auf Militia warten, deswegen verdoppel ich die Rate.
    upsert(updater, "Militia Training Settings", "MILITIA_TRAINING_RATE", "8")
    upsert(updater, "Financial Settings", "MILITIA_BASE_TRAINING_COST", "375")

    # Manchmal greifen die Gegner mit 15 Elite-Soldaten an. Da reichen 20 hellblaue nicht.
    # Ich will meine Mercs spielen, keine Militia...
    upsert(updater, "Militia Training Settings", "ALLOW_TRAINING_ELITE_MILITIA", "FALSE")
    upsert(updater, "Militia Training Settings", "MAX_MILITIA_PER_SECTOR", "30")
    upsert(updater, "Militia Training Settings", "NUM_MILITIA_TRAINED_PER_SESSION", "15")

    # Ich will keine Militia managen, sondern meine Mercs…
    upsert(updater, "Mobile Militia Training Settings", "ALLOW_MOBILE_MILITIA", "FALSE")

    # Hell no, lasst meine Items in Ruhe.
    upsert(updater, "Militia Equipment Settings", "MILITIA_USE_SECTOR_EQUIPMENT", "FALSE")

    # Startgeld
    # 50k reicht fuer IMP + 4 guenstige Mercs oder IMP + 1 teurer Merc ueber 2 Wochen
    upsert(updater, "Financial Settings", "STARTING_CASH_NOVICE", "50000")
    upsert(updater, "Financial Settings", "STARTING_CASH_EXPERIENCED", "50000")
    upsert(updater, "Financial Settings", "STARTING_CASH_EXPERT", "50000")
    upsert(updater, "Financial Settings", "STARTING_CASH_INSANE", "50000")

    # RNG! Kann einen Unterschied von ~12k/Tag machen wenn es die beste statt der schlechtesten
    # Mine trifft…
    # Dann lieber Income runter von den spaeteren Minen. Kann man in Scripts/initmines.lua machen.
    upsert(updater, "Strategic Event Settings", "WHICH_MINE_SHUTS_DOWN", "0")
    upsert(updater, "Financial Settings", "MINE_INCOME_PERCENTAGE", "100")

    # Wenn Militia Unterhalt kosten wuerden, wuerde das nur mehr Militia-Micromanagement
    # incentivieren. Interessiert mich aber nicht. Ich will die Stadt voll besetzen und
    # mich nicht mehr drum kuemmern muessen.
    upsert(updater, "Financial Settings", "DAILY_MILITIA_UPKEEP_TOWN_GREEN", "0")
    upsert(updater, "Financial Settings", "DAILY_MILITIA_UPKEEP_TOWN_REGULAR", "0")
    upsert(updater, "Financial Settings", "DAILY_MILITIA_UPKEEP_TOWN_ELITE", "0")

    # Ich will keine Assassinen unter den Militia...
    # Kaempfe eh nie zusammen mit denen, also ist egal.
    upsert(updater, "Tactical Difficulty Settings", "ENEMY_ASSASSINS", "FALSE")

    # Schneller!
    upsert(updater, "Graphics Settings", "MILITIA_TURN_SPEED_UP_FACTOR", "0.0")
    upsert(updater, "Clock Settings", "AUTO_FAST_FORWARD_ENEMIES", "1")
    upsert(updater, "Clock Settings", "AUTO_FAST_FORWARD_MILITIA", "2")
    upsert(updater, "Clock Settings", "AUTO_FAST_FORWARD_CIVS", "2")
    upsert(updater, "Clock Settings", "AUTO_FAST_FORWARD_CREATURES", "1")

    # Diese Stats sind fast nur mit Grind verbesserbar, was ich nicht mache,
    # also mach sie einfacher!
    upsert(updater, "Tactical Difficulty Settings", "HEALTH_SUBPOINTS_TO_IMPROVE", "35")
    upsert(updater, "Tactical Difficulty Settings", "STRENGTH_SUBPOINTS_TO_IMPROVE", "35")
    upsert(updater, "Tactical Difficulty Settings", "WISDOM_SUBPOINTS_TO_IMPROVE", "35")
    upsert(updater, "Tactical Difficulty Settings", "DEXTERITY_SUBPOINTS_TO_IMPROVE", "35")
    upsert(updater, "Tactical Difficulty Settings", "AGILITY_SUBPOINTS_TO_IMPROVE", "35")

    # Suppression Fire ist eigentlich eine coole Mechanik.
    # Es bufft Automatikwaffen.
    # Es macht Kaempfe aber weniger dynamisch.
    # Gegner profitieren mehr davon, weil sie mehr sind und mehr sprayen.
    # Deswegen aktiviere ich nur ein bisschen Suppression und mache es gegen AI effektiver.
    # Habe 200 gegen Spieler getestet und es war viel zu viel! Vanilla ist 0!
    upsert(updater, "Tactical Suppression Fire Settings", "SUPPRESSION_EFFECTIVENESS", "50")
    upsert(updater, "Tactical Suppression Fire Settings", "SUPPRESSION_EFFECTIVENESS_PLAYER", "100")
    upsert(updater, "Tactical Suppression Fire Settings", "SUPPRESSION_EFFECTIVENESS_AI", "200")
    upsert(updater, "Tactical Suppression Fire Settings", "NOTIFY_WHEN_PINNED_DOWN", "TRUE")
    upsert(updater, "Tactical Suppression Fire Settings", "MIN_DISTANCE_FRIENDLY_SUPPRESSION", "30")
    # Ich will, dass Suppression Fire von Anfang bis Ende etwa konstant bleibt.
    # Nicht dass am Anfang jeder ne Pussie ist und am Ende das Feature nicht mehr zu spueren ist.
    upsert(updater, "Tactical Suppression Fire Settings", "SUPPRESSION_TOLERANCE_MIN", "8")
    upsert(updater, "Tactical Suppression Fire Settings", "SUPPRESSION_TOLERANCE_MAX", "12")
    # Cooles Feature
    upsert(updater, "Tactical Suppression Fire Settings", "NEARBY_FRIENDLIES_AFFECT_TOLERANCE", "TRUE")
    # Ist ein Buff fuer Granaten.
    upsert(updater, "Tactical Suppression Fire Settings", "EXPLOSIVE_SUPPRESSION_EFFECTIVENESS", "50")
    # Suppression macht Sinn mit Rifles
    upsert(updater, "Tactical Suppression Fire Settings", "AI_SUPPRESS_MIN_MAG_SIZE", "30")
    upsert(updater, "Tactical Suppression Fire Settings", "AI_SUPPRESS_MIN_AMMO_REMAINING", "10")
    # Shock verursacht, dass alle schlechter zielen und getroffen werden. Dummes Feature.
    # Ich wuerde es gerne fuer die Animation und den Flair anlassen und die Effekte deaktivieren,
    # aber ich weiss nicht, ob man wirklich alle Effekte deaktiviert bekommt, also raus damit!
    upsert(updater, "Tactical Suppression Fire Settings", "SUPPRESSION_SHOCK_INTENSITY", "0")
    upsert(updater, "Tactical Suppression Fire Settings", "MAX_SUPPRESSION_SHOCK", "30")
    upsert(updater, "Tactical Suppression Fire Settings", "COWERING_PENALTY_TO_SUPPRESSION_TOLERANCE", "0")
    upsert(updater, "Tactical Suppression Fire Settings", "SHOCK_REDUCES_SIGHTRANGE", "0")
    upsert(updater, "Tactical Suppression Fire Settings", "MAX_CTH_PENALTY_FROM_SHOCK", "1")
    upsert(updater, "Tactical Suppression Fire Settings", "CTH_PENALTY_PER_TARGET_SHOCK", "0")
    upsert(updater, "Tactical Suppression Fire Settings", "MAX_CTH_PENALTY_FOR_TARGET_SHOCK", "1")
    upsert(updater, "Tactical Suppression Fire Settings", "CTH_PENALTY_DIVISOR_FOR_PRONE_SHOCKED_TARGET", "1")
    upsert(updater, "Tactical Suppression Fire Settings", "CTH_PENALTY_DIVISOR_FOR_CROUCHED_SHOCKED_TARGET_HEAD", "1")
    upsert(updater, "Tactical Suppression Fire Settings", "CTH_PENALTY_DIVISOR_FOR_CROUCHED_SHOCKED_TARGET_TORSO", "1")
    upsert(updater, "Tactical Suppression Fire Settings", "CTH_PENALTY_FOR_COWERING_CROUCHED_TARGET_LEGS_DIVISOR", "1")
    upsert(updater, "Tactical Interface Settings", "SHOW_HEALTHBARSOVERHEAD", "1")

    # Nervt, wenn Gegner durch Luck gewinnen.
    upsert(updater, "Strategic Gameplay Settings", "AUTORESOLVE_LUCK_FACTOR", "1.25")

    # Mercs koennen mehr tragen. Ist praktischer.
    upsert(updater, "Item Property Settings", "STRENGTH_TO_LIFT_HALF_KILO", "0.8")

    # Nervt, wenn er nicht da ist.
    upsert(updater, "Shopkeeper Inventory Settings", "CHANCE_TONY_AVAILABLE", "100")

    # Schnellerer Laptop.
    upsert(updater, "Laptop Settings", "FAST_WWW_SITES_LOADING", "TRUE")
    upsert(updater, "Laptop Settings", "DISABLE_LAPTOP_TRANSITION", "TRUE")

    # Beliebiger Heli Drop klingt lustig!
    upsert(updater, "Strategic Gameplay Settings", "ALLOW_SKYRIDER_HOT_LZ", "3")

    # Yes, make it useful!
    upsert(updater, "Strategic Gameplay Settings", "HUMVEE_OFFROAD", "TRUE")

    # Nicht noch mehr RNG Jams please!
    upsert(updater, "Strategic Gameplay Settings", "DIRT_SYSTEM", "FALSE")
    upsert(updater, "Strategic Gameplay Settings", "ADVANCED_REPAIR", "FALSE")
    upsert(updater, "Strategic Gameplay Settings", "ONLY_REPAIR_GUNS_AND_ARMOUR", "FALSE")

    # Why not.
    upsert(updater, "Strategic Gameplay Settings", "ENABLE_ALL_TERRORISTS", "TRUE")

    # Klingt interessant. Mal testen in einem Playthrough!
    # Der Vanilla Progress hat sich aber schon sehr gut angefuehlt.
    # TODO
    upsert(updater, "Strategic Progress Settings", "ALTERNATE_PROGRESS_CALCULATION", "TRUE")

    # Von ueberall Items loeschen zu koennen ist komfortabler!
    upsert(updater, "Strategic Gameplay Settings", "NO_REMOVE_RANDOM_SECTOR_ITEMS", "FALSE")

    # 180 Grad Sicht statt 360 Grad wie bei Vanilla.
    # Manchmal ein bisschen nervig, aber erlaubt taktisch neue Manoever.
    # Wenn der Merc gerade in ein Zielfernrohr schaut,
    # ist sein Sichtfeld weiter, aber noch schmaler!
    upsert(updater, "Tactical Vision Settings", "ALLOW_TUNNEL_VISION", "TRUE")
    upsert(updater, "Tactical Vision Settings", "BASE_SIGHT_RANGE", "13")

    # The realistic tracers don't sound like a good gameplay feature.
    upsert(updater, "Tactical Gameplay Settings", "REALISTIC_TRACERS", "0")

    # Nervt.
    upsert(updater, "Tactical Interface Settings", "INACCURATE_CTH_READOUT", "FALSE")

    # 30 ist viel zu lange.
    # Mit moderner Hardware sollte das kein Problem sein!
    upsert(updater, "Troubleshooting Settings", "DEAD_LOCK_DELAY", "10")

    # Prone cover bonus macht Sinn.
    # Bei den anderen beiden bin ich mir noch nicht sicher was gute Werte sind...
    upsert(updater, "Tactical Cover System Settings", "COVER_SYSTEM_STANCE_EFFECTIVENESS", "10")
    upsert(updater, "Tactical Cover System Settings", "COVER_SYSTEM_TREE_EFFECTIVENESS", "25")
    upsert(updater, "Tactical Cover System Settings", "COVER_SYSTEM_MOVEMENT_EFFECTIVENESS", "20")

    # Das Feature klingt eher lame, also reduzier den Effekt!
    upsert(updater, "Tactical Gameplay Settings", "ENERGY_COST_FOR_WEAPON_RECOIL_KICK", "20")
    upsert(updater, "Tactical Gameplay Settings", "ENERGY_COST_FOR_WEAPON_WEIGHT", "20")

    # Aim Bonus fuer Prone oder Crouch mit einer Stuetze vor sich.
    # Ich finde das klingt nach nem coolen Feature.
    upsert(updater, "Tactical Gameplay Settings", "WEAPON_RESTING", "TRUE")
    upsert(updater, "Tactical Gameplay Settings", "WEAPON_RESTING_DISPLAY", "TRUE")
    upsert(updater, "Tactical Gameplay Settings", "WEAPON_RESTING_PRONE_BONI_PERCENTAGE", "50")

    # Klingt gut?
    upsert(updater, "Tactical Gameplay Settings", "ENHANCED_CLOSE_COMBAT_SYSTEM", "TRUE")

    # Klingt gut!
    upsert(updater, "Tactical Gameplay Settings", "CAN_JUMP_THROUGH_WINDOWS", "TRUE")
    upsert(updater, "Tactical Gameplay Settings", "CAN_JUMP_THROUGH_CLOSED_WINDOWS", "TRUE")

    # Klingt gut.
    upsert(updater, "Tactical Gameplay Settings", "CTH_PENALTY_FOR_TARGET_MOVEMENT", "1.5")
    upsert(updater, "Tactical Gameplay Settings", "MAX_CTH_PENALTY_FOR_MOVING_TARGET", "30")

    # Klingt cool.
    upsert(updater, "Tactical Gameplay Settings", "ALLOW_WALKING_WITH_WEAPON_RAISED", "TRUE")

    # Aim Settings. Bin mir bei allem noch nicht so sicher.
    # TODO
    # Was heisst depend on distance? Was bewirkt das? Buff/nerf fuer nah/fern?
    upsert(updater, "Tactical Gameplay Settings", "AIM_LEVELS_DEPEND_ON_DISTANCE", "TRUE")
    # Wer profitiert/verliert davon? Sniper? Pistols?
    upsert(updater, "Tactical Gameplay Settings", "DYNAMIC_AIMING_LIMITS", "TRUE")
    # True waere ein nerf fuer Scopes. Notwendig?
    upsert(updater, "Tactical Gameplay Settings", "INCREASE_AIMING_COSTS", "FALSE")
    # Spielt sich das gut?
    upsert(updater, "Tactical Gameplay Settings", "USE_SCOPE_MODES", "TRUE")
    upsert(updater, "Tactical Gameplay Settings", "DISPLAY_SCOPE_MODES", "TRUE")
    upsert(updater, "Tactical Gameplay Settings", "ALLOW_ALTERNATIVE_WEAPON_HOLDING", "0")
    # Aimed burst/auto... Notwendig oder imba? Fuer Burst oder fuer Auto?
    upsert(updater, "Tactical Interface Settings", "USE_AIMED_BURST", "TRUE")

    # Headshots brauchen keinen Buff!
    upsert(updater, "Tactical Gameplay Settings", "CHANCE_BLINDED_BY_HEADSHOT", "0")

    # Praktisch!
    upsert(updater, "Tactical Gameplay Settings", "KNOWN_NPCS_DIFFERENT_MAPCOLOUR", "TRUE")

    # Praktisch!
    upsert(updater, "Tactical Gameplay Settings", "SHOW_ENEMY_AWARENESS", "TRUE")

    # Brauch ich nich...
    upsert(updater, "Tactical Gameplay Settings", "SHOW_ENEMY_RANK_ICON", "0")

    # Vanilla Style
    upsert(updater, "Tactical Interface Settings", "SHOW_ENEMY_HEALTH", "1")

    # Praktisch
    upsert(updater, "Tactical Interface Settings", "REVEAL_DROPPED_ENEMY_ITEMS_AFTER_COMBAT", "TRUE")
    upsert(updater, "Tactical Interface Settings", "MINES_SPOTTED_NO_TALK", "TRUE")
    upsert(updater, "Tactical Interface Settings", "AUTOMATICALLY_FLAG_MINES_WHEN_SPOTTED", "TRUE")
    upsert(updater, "Tactical Interface Settings", "STAND_UP_AFTER_BATTLE", "TRUE")
    upsert(updater, "Tactical Interface Settings", "USE_NEW_BURST-AUTO_TARGETING_CURSORS", "1")
    upsert(updater, "Tactical Interface Settings", "SHOW_COVER_INDICATOR", "1")
    upsert(updater, "Tactical Interface Settings", "ENEMY_HIT_COUNT", "0")

    # Ist zwar etwas unrealistisch, aber ist bei Vanilla so.
    # Und die Option beeinflusst auch nur Mercs, nicht Gegner, also macht es schwieriger.
    # Erlaubt quasi, dass man fuer seine Kameraden spottet, ohne das 1.13 Spotter Feature.
    upsert(updater, "Tactical Interface Settings", "SHOOT_UNSEEN_PENALTY", "0")

    # Als ob meine Jungs die Seite wechseln wuerden, wenn ich aus Versehen einen kille...
    upsert(updater, "Tactical Difficulty Settings", "CAN_MILITIA_BECOME_HOSTILE", "0")

    # Die sind doch stark genug...
    upsert(updater, "Tactical Difficulty Settings", "SPECIAL_NPCS_STRONGER", "0")

    # Kein RNG Blocker please
    upsert(updater, "Tactical Weapon Overheating Settings", "OVERHEATING", "FALSE")

    # Praktisch
    upsert(updater, "Strategic Interface Settings", "ALLOW_DESCRIPTION_BOX_FOR_ITEMS_IN_SECTOR_INVENTORY", "TRUE")
    upsert(updater, "Strategic Interface Settings", "INCLUDE_CONTRACTS_IN_PROJECTED_EXPENSES_WINDOW", "2")
    upsert(updater, "Strategic Interface Settings", "DISABLE_STRATEGIC_TRANSITION", "TRUE")

    # Ich spiele mit dem alten Inventar, also kann ich auch nur 4 Attachments kriegen!
    upsert(updater, "Item Property Settings", "MAX_ENEMY_ATTACHMENTS", "4")

    # Auch auf Novice sollen alle vorplatzierten Gegner erscheinen!
    upsert(updater, "Strategic Enemy AI Settings", "INITIAL_GARRISON_PERCENTAGES_NOVICE", "100")
    upsert(updater, "Strategic Enemy AI Settings", "INITIAL_GARRISON_PERCENTAGES_EXPERIENCED", "100")

    # Macht Sachen schneller
    upsert(updater, "Strategic Assignment Settings", "MINUTES_FOR_ASSIGNMENT_TO_COUNT", "5")

    # Auch Nuller-Stats soll man trainieren koennen!
    upsert(updater, "Strategic Assignment Settings", "MIN_REQUIRED_SKILL_TO_BEGIN_TRAINING", "0")

    # Praktisch
    upsert(updater, "Strategic Assignment Settings", "SYNCHRONIZED_SLEEPING_HOURS_WHEN_TRAINING_TOGETHER", "1")
    upsert(updater, "Strategic Assignment Settings", "SYNCHRONIZED_WAKING_HOURS_WHEN_TRAINING_TOGETHER", "1")
    upsert(updater, "Strategic Assignment Settings", "REST_IF_NO_TRAINING_PARTNER_AVAILABLE", "1")

    # Praktisches Feature, um den letzten Gegner zu finden
    upsert(updater, "Overhead Map Settings", "MARKER_MODE", "2")
    upsert(updater, "Overhead Map Settings", "DAYTIME_PRECISION", "4")
    upsert(updater, "Overhead Map Settings", "NIGHTTIME_PRECISION", "4")
    upsert(updater, "Overhead Map Settings", "MAX_SOLDIERS_LEFT", "1")

    # Ich will nicht point-blank und full-focused danebenschiessen...
    upsert(updater, "Tactical Gameplay Settings", "MAXIMUM_POSSIBLE_CTH", "100")
    upsert(updater, "Tactical Gameplay Settings", "MINIMUM_POSSIBLE_CTH", "1")

    # Gegner Tooltips (Alt-Taste halten)
    # Wenn ich einen Gegner sehe, will ich auch sein Equip sehen.
    upsert(updater, "Tactical Tooltip Settings", "SOLDIER_TOOLTIP_DETAIL_LEVEL", "3")
    upsert(updater, "Tactical Tooltip Settings", "DYNAMIC_SOLDIER_TOOLTIPS", "FALSE")
    upsert(updater, "Tactical Tooltip Settings", "ALLOW_DYNAMIC_TOOLTIP_DETAIL_LEVEL", "FALSE")
    upsert(updater, "Tactical Tooltip Settings", "ALLOW_DYNAMIC_TOOLTIP_RANGE", "FALSE")

    # Praktisch
    upsert(updater, "Tactical Difficulty Settings", "NO_AUTO_FOCUS_CHANGE_IN_REALTIME_SNEAK", "TRUE")
    upsert(updater, "Tactical Difficulty Settings", "QUIET_REAL_TIME_SNEAK", "TRUE")

    # Macht die AI bissl schlauer hoffentlich.
    upsert(updater, "Tactical Interface Settings", "NEW_AI_TACTICAL", "TRUE")

    # Praktisch
    upsert(updater, "Tactical Interface Settings", "CHANCE_SAY_ANNOYING_PHRASE", "40")
    upsert(updater, "Tactical Interface Settings", "ALLOW_LAZY_CIVILIANS", "TRUE")
    upsert(updater, "Tactical Interface Settings", "WE_SEE_WHAT_MILITIA_SEES_AND_VICE_VERSA", "TRUE")

    # Ich mag den Vanilla Style mehr
    upsert(updater, "Tactical Interface Settings", "NOCTOVISION_NIGHT_RADAR_MAP", "FALSE")
    upsert(updater, "Tactical Interface Settings", "MONOCHROMATIC_RADAR_MAP", "FALSE")
    upsert(updater, "Tactical Interface Settings", "MONOCHROMATIC_OVERHEAD_MAP", "FALSE")

    # VSync off
    upsert(updater, "Graphics Settings", "VERTICAL_SYNC", "FALSE")

    # Praktisch
    upsert(updater, "Financial Settings", "SELL_ITEMS_WITH_ALT_LMB", "TRUE")
    upsert(updater, "Financial Settings", "SELL_ITEMS_PRICE_MODIFIER", "10")

    # Keine zu krassen Werte, weil bei Stuermen sind die Werte verdoppelt!
    upsert(updater, "Tactical Weather Settings", "ALLOW_RAIN", "TRUE")
    upsert(updater, "Tactical Weather Settings", "WEAPON_RELIABILITY_REDUCTION_PER_RAIN_INTENSITY", "0")
    upsert(updater, "Tactical Weather Settings", "BREATH_GAIN_REDUCTION_PER_RAIN_INTENSITY", "17")
    upsert(updater, "Tactical Weather Settings", "VISUAL_DISTANCE_DECREASE_PER_RAIN_INTENSITY", "17")

    # Vanilla ist glaub 100? 1.13 Default ist 5. Aber dann sind Camo Kits ja mega useless...
    # Zu gut sollte man es aber wsl nicht machen, weil sonst Ghili Suits unnoetig werden.
    upsert(updater, "Tactical Gameplay Settings", "CAMO_KIT_USABLE_AREA", "20")

    shutil.copy2(args.filepath, f'{args.filepath}.BACKUP{time.time_ns()}')
    updater.update_file()

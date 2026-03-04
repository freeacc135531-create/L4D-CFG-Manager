CMD_DATA = {

    "Movement": [
        ("+forward", "Move forward"),
        ("+back", "Move backward"),
        ("+moveleft", "Strafe left"),
        ("+moveright", "Strafe right"),
        ("+jump", "Jump"),
        ("+duck", "Crouch"),
        ("+speed", "Walk"),
        ("+use", "Use / Interact"),
    ],

    "Combat": [
        ("+attack", "Primary attack"),
        ("+attack2", "Secondary attack"),
        ("+reload", "Reload weapon"),
        ("+zoom", "Zoom"),
        ("+melee", "Melee attack"),
        ("+lookatweapon", "Inspect weapon"),
    ],

    "Communication": [
        ("say", "Chat message"),
        ("say_team", "Team chat"),
        ("vocalize SmartLook", "Call out"),
        ("vocalize PlayerHelp", "Call for help"),
        ("vocalize PlayerThanks", "Say thanks"),
    ],

    "Weapons": [
        ("slot1", "Primary weapon"),
        ("slot2", "Secondary weapon"),
        ("slot3", "Throwable"),
        ("slot4", "Medkit / Pills"),
        ("slot5", "Utility"),
        ("lastinv", "Last weapon used"),
        ("drop", "Drop weapon"),
    ],

    "Game Actions": [
        ("retry", "Reconnect to server"),
        ("disconnect", "Disconnect"),
        ("callvote", "Start vote"),
        ("chooseteam", "Change team"),
        ("spectate", "Spectator mode"),
    ],

    "HUD & View": [
        ("cl_drawhud 0", "Hide HUD"),
        ("cl_drawhud 1", "Show HUD"),
        ("r_drawviewmodel 0", "Hide weapon model"),
        ("r_drawviewmodel 1", "Show weapon model"),
        ("thirdperson", "Third person (if enabled)"),
        ("firstperson", "First person"),
    ],

    "Network": [
        ("rate 30000", "Set rate 30000"),
        ("cl_cmdrate 66", "Set cmdrate 66"),
        ("cl_updaterate 66", "Set updaterate 66"),
        ("cl_interp 0", "Set interp 0"),
        ("cl_interp_ratio 1", "Set interp ratio 1"),
    ],

    "Fun / Troll": [
        ("explode", "Explode (cheats)"),
        ("kill", "Suicide"),
        ("noclip", "Noclip (cheats)"),
        ("sv_cheats 1", "Enable cheats"),
        ("impulse 101", "Give items (if enabled)"),
    ]
}
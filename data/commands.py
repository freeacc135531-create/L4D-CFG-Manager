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
        ("+strafe", "Strafe modifier"),
        ("+moveup", "Swim up"),
        ("+movedown", "Swim down"),
    ],

    "Combat": [
        ("+attack", "Primary attack"),
        ("+attack2", "Secondary attack"),
        ("+reload", "Reload weapon"),
        ("+zoom", "Zoom weapon"),
        ("+melee", "Melee attack"),
        ("+lookatweapon", "Inspect weapon"),
    ],

    "Weapons": [
        ("slot1", "Primary weapon"),
        ("slot2", "Secondary weapon"),
        ("slot3", "Throwable"),
        ("slot4", "Medkit / Pills"),
        ("slot5", "Utility"),
        ("lastinv", "Last weapon used"),
        ("drop", "Drop weapon"),
        ("invnext", "Next weapon"),
        ("invprev", "Previous weapon"),
    ],

    "Communication": [
        ("say", "Chat message"),
        ("say_team", "Team chat"),
        ("vocalize SmartLook", "Call out"),
        ("vocalize PlayerHelp", "Call for help"),
        ("vocalize PlayerThanks", "Say thanks"),
        ("vocalize PlayerSorry", "Say sorry"),
        ("vocalize PlayerLaugh", "Laugh"),
        ("vocalize PlayerTaunt", "Taunt"),
    ],

    "Camera & View": [
        ("firstperson", "Switch to first person"),
        ("thirdperson", "Switch to third person"),
        ("thirdpersonshoulder", "Third person shoulder"),
        ("toggle r_drawviewmodel 0 1", "Toggle weapon model"),
        ("toggle cl_drawhud 0 1", "Toggle HUD"),
        ("toggle mat_fullbright 0 1", "Toggle fullbright"),
    ],

    "Utility": [
        ("toggleconsole", "Open console"),
        ("jpeg", "Take screenshot"),
        ("screenshot", "Take screenshot (TGA)"),
        ("incrementvar volume 0 1 0.1", "Increase volume"),
        ("incrementvar volume 0 1 -0.1", "Decrease volume"),
        ("record demo", "Start demo recording"),
        ("stop", "Stop demo recording"),
    ],

    "Network": [
        ("rate 30000", "Set rate 30000"),
        ("rate 60000", "Set rate 60000"),
        ("rate 100000", "Set rate 100000"),
        ("cl_cmdrate 30", "Set cmdrate 30"),
        ("cl_cmdrate 60", "Set cmdrate 60"),
        ("cl_cmdrate 66", "Set cmdrate 66"),
        ("cl_updaterate 30", "Set updaterate 30"),
        ("cl_updaterate 60", "Set updaterate 60"),
        ("cl_updaterate 66", "Set updaterate 66"),
        ("cl_interp 0", "Set interp 0"),
        ("cl_interp_ratio 1", "Set interp ratio 1"),
        ("cl_interp_ratio 2", "Set interp ratio 2"),
    ],

    "Spectator": [
        ("spec_next", "Next player"),
        ("spec_prev", "Previous player"),
        ("spec_mode", "Change spectator mode"),
        ("spec_player", "Spectate specific player"),
    ],

    "Game Actions": [
        ("retry", "Reconnect to server"),
        ("disconnect", "Disconnect from server"),
        ("callvote", "Start vote"),
        ("chooseteam", "Change team"),
        ("spectate", "Join spectator"),
    ],

    "Fun / Troll": [
        ("kill", "Suicide"),
        ("explode", "Explode (cheats)"),
        ("noclip", "Noclip (cheats)"),
        ("sv_cheats 1", "Enable cheats"),
        ("impulse 101", "Give items (cheats)"),
    ]
}
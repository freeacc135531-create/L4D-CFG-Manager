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
        ("slot6", "Custom"),
        ("slot7", "Custom"),
        ("slot8", "Custom"),
        ("slot9", "Custom"),
        ("slot0", "Custom"),
        ("lastinv", "Last weapon used"),
        ("drop", "Drop weapon (for scripts or modded server"),
        ("invnext", "Next weapon"),
        ("invprev", "Previous weapon"),
    ],

    "Communication": [
        ("messagemode", "General chat"),
        ("messagemode2", "Team chat"),
        ("say !r", "Say ready in chat"),
        ("say !unr", "Say unready in chat"),
        ("+mouse_menu QA", "Vocalizer 1"),
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
        ("incrementvar volume 0 1 0.1", "Increase volume"),
        ("incrementvar volume 0 1 -0.1", "Decrease volume"),
        ("record demo", "Start demo recording"),
        ("stop", "Stop demo recording"),
        ("snd_restart", "Restart sounds"),
        ("toggle voice_modenable 0 1", "Toggle voice chat"),
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

    "Game Actions": [
        ("disconnect", "Disconnect from server"),
        ("chooseteam", "Change team"),
        ("spectate", "Join spectator"),
        ("jointeam 2", "Join survivors"),
        ("jointeam 3", "Join infected"),
    ],

    "Fun / Troll": [
        ("kill", "Suicide"),
        ("noclip", "Noclip (cheats)"),
        ("sv_cheats 1", "Enable cheats"),
        ("impulse 101", "Give items (cheats)"),
    ],
    
        "Modded Server": [
        ("say !buy", "Buy menu"),
        ("say !buy ak", "Buy ak47"),
        ("say !buy katana", "Buy katana"),
        ("say !buy molotov", "Buy molotov"),
    ]
}
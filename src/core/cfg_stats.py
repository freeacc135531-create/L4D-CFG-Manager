def get_cfg_stats(cfg_data):

    stats = {
        "total_commands": 0,
        "network": 0,
        "input": 0,
        "audio": 0,
        "graphics": 0,
        "other": 0
    }

    network_cmds = {
        "rate", "cl_cmdrate", "cl_updaterate",
        "cl_interp", "cl_interp_ratio"
    }

    input_cmds = {
        "sensitivity", "m_rawinput", "m_filter"
    }

    audio_cmds = {
        "volume", "snd_mixahead"
    }

    graphics_cmds = {
        "fps_max", "mat_queue_mode", "cl_forcepreload"
    }

    for cmd in cfg_data:

        stats["total_commands"] += 1

        if cmd in network_cmds:
            stats["network"] += 1

        elif cmd in input_cmds:
            stats["input"] += 1

        elif cmd in audio_cmds:
            stats["audio"] += 1

        elif cmd in graphics_cmds:
            stats["graphics"] += 1

        else:
            stats["other"] += 1

    return stats
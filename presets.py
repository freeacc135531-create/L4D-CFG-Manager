LOW_LATENCY = {
    "rate": "100000",
    "cl_cmdrate": "100",
    "cl_updaterate": "100",
    "cl_interp_ratio": "1",
    "cl_interp": "0",
    "mat_queue_mode": "2",
    "fps_max": "300",
    "m_rawinput": "1",
    "m_filter": "0",
    "cl_forcepreload": "1",
    "r_threaded_particles": "1"
}

FPS_MAX = {
    "mat_picmip": "-1",
    "mat_antialias": "0",
    "mat_forceaniso": "0",
    "r_shadowrendertotexture": "0",
    "r_dynamic": "0",
    "r_propsmaxdist": "0",
    "cl_forcepreload": "1",
    "mat_queue_mode": "2",
    "fps_max": "300"
}

NETWORK_STABLE = {
    "rate": "80000",
    "cl_cmdrate": "66",
    "cl_updaterate": "66",
    "cl_interp_ratio": "2",
    "cl_interp": "0.033",
    "mat_queue_mode": "2"
}

COMPETITIVE = {
    "rate": "100000",
    "cl_cmdrate": "100",
    "cl_updaterate": "100",
    "cl_interp_ratio": "1",
    "cl_interp": "0",
    "mat_queue_mode": "2",
    "m_rawinput": "1",
    "m_filter": "0",
    "cl_forcepreload": "1",
    "fps_max": "300",
    "r_threaded_particles": "1",
    "snd_mixahead": "0.05"
}

ULTRA_LOW_END_PC = {
    "mat_picmip": "2",
    "mat_antialias": "0",
    "mat_forceaniso": "0",
    "r_dynamic": "0",
    "r_shadowrendertotexture": "0",
    "r_propsmaxdist": "0",
    "cl_forcepreload": "1",
    "mat_queue_mode": "2",
    "fps_max": "120"
}

PRESETS = {
    "Competitive Low Latency": LOW_LATENCY,
    "FPS Max": FPS_MAX,
    "Network Stable": NETWORK_STABLE,
    "Competitive": COMPETITIVE,
    "Ultra Low End PC": ULTRA_LOW_END_PC
}
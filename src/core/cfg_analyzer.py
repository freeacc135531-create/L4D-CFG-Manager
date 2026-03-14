def parse_cfg(path):
    config = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("//"):
                continue

            parts = line.split(None, 1)
            if len(parts) == 2:
                config[parts[0]] = parts[1].strip().strip('"')

    return config


def compare_configs(current_config, reference_config):
    issues = []

    for key, ref_value in reference_config.items():
        current_value = current_config.get(key)

        if current_value is None:
            issues.append(f"Missing: {key} (recommended {ref_value})")
        elif current_value != ref_value:
            issues.append(
                f"{key} = {current_value} (recommended {ref_value})"
            )

    return issues
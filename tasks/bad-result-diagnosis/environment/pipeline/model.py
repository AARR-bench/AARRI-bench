from __future__ import annotations


def describe_wiring(config: dict[str, object]) -> dict[str, object]:
    return {
        "rgb_stream": "pretrained_rgb_backbone",
        "sar_stream": "adapter_branch",
        "adapter_trainable": not bool(config.get("freeze_adapter", True)),
        "fusion_stage": config.get("fusion_stage", "early_concat"),
    }

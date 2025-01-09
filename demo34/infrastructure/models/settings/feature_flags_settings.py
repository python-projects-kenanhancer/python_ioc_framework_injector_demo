from typing import Any

from pydantic import BaseModel


class FeatureFlagsSettings(BaseModel):
    split_balances_enabled: bool
    circuit_breaker_enabled: bool
    circuit_breaker_checks_subset_config: dict[str, Any]
    circuit_breaker_duration: int

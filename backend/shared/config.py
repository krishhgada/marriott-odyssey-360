"""
Feature flags and configuration for new features
"""

import os
from typing import Optional


class FeatureFlags:
    """Feature flags for new capabilities"""
    
    # New feature flags (default True for development)
    FEATURE_PRIVACY: bool = os.getenv("FEATURE_PRIVACY", "true").lower() == "true"
    FEATURE_CULTURE: bool = os.getenv("FEATURE_CULTURE", "true").lower() == "true"
    FEATURE_TRUSTLENS: bool = os.getenv("FEATURE_TRUSTLENS", "true").lower() == "true"
    FEATURE_INTERMODAL: bool = os.getenv("FEATURE_INTERMODAL", "true").lower() == "true"
    FEATURE_AGENTOPS: bool = os.getenv("FEATURE_AGENTOPS", "true").lower() == "true"
    FEATURE_INSIGHTS: bool = os.getenv("FEATURE_INSIGHTS", "true").lower() == "true"
    
    # Demo token for local testing
    DEMO_TOKEN: str = os.getenv("DEMO_TOKEN", "demo-token-odyssey360")
    
    # Service configuration
    TELEMETRY_ENABLED: bool = os.getenv("TELEMETRY_ENABLED", "true").lower() == "true"
    
    @classmethod
    def get_enabled_features(cls) -> dict:
        """Get dictionary of all feature flags"""
        return {
            "privacy": cls.FEATURE_PRIVACY,
            "culture": cls.FEATURE_CULTURE,
            "trustlens": cls.FEATURE_TRUSTLENS,
            "intermodal": cls.FEATURE_INTERMODAL,
            "agentops": cls.FEATURE_AGENTOPS,
            "insights": cls.FEATURE_INSIGHTS,
        }
    
    @classmethod
    def is_enabled(cls, feature: str) -> bool:
        """Check if a specific feature is enabled"""
        feature_map = {
            "privacy": cls.FEATURE_PRIVACY,
            "culture": cls.FEATURE_CULTURE,
            "trustlens": cls.FEATURE_TRUSTLENS,
            "intermodal": cls.FEATURE_INTERMODAL,
            "agentops": cls.FEATURE_AGENTOPS,
            "insights": cls.FEATURE_INSIGHTS,
        }
        return feature_map.get(feature.lower(), False)


# Global instance
flags = FeatureFlags()



"""
Telemetry and metrics tracking for Marriott's Odyssey 360 AI
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
import asyncio
from threading import Lock

# In-memory storage
_events: List[Dict[str, Any]] = []
_counters: Dict[str, int] = defaultdict(int)
_lock = Lock()

# Telemetry directory
TELEMETRY_DIR = Path("./.telemetry")
TELEMETRY_FILE = TELEMETRY_DIR / "telemetry.csv"

# Ensure telemetry directory exists
TELEMETRY_DIR.mkdir(exist_ok=True)

# Initialize CSV file with headers if it doesn't exist
if not TELEMETRY_FILE.exists():
    with open(TELEMETRY_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'event_type', 'path', 'method', 'status', 'latency_ms', 'user_id', 'metadata'])


def telemetry(event: dict) -> None:
    """
    Log a telemetry event
    
    Args:
        event: Dictionary containing event data
            Required keys: event_type
            Optional: path, method, status, latency_ms, user_id, metadata
    
    Example:
        telemetry({
            "event_type": "api_request",
            "path": "/api/privacy/recommend",
            "method": "POST",
            "status": 200,
            "latency_ms": 45.2,
            "user_id": "demo-user"
        })
    """
    with _lock:
        # Add timestamp
        event['timestamp'] = datetime.utcnow().isoformat()
        
        # Store in memory (keep last 1000 events)
        _events.append(event)
        if len(_events) > 1000:
            _events.pop(0)
        
        # Update counters
        event_type = event.get('event_type', 'unknown')
        _counters[f"event_{event_type}"] += 1
        _counters['total_events'] += 1
        
        # Increment status counter if present
        if 'status' in event:
            status_category = f"status_{event['status'] // 100}xx"
            _counters[status_category] += 1
        
        # Write to CSV file (async to avoid blocking)
        try:
            with open(TELEMETRY_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    event.get('timestamp', ''),
                    event.get('event_type', ''),
                    event.get('path', ''),
                    event.get('method', ''),
                    event.get('status', ''),
                    event.get('latency_ms', ''),
                    event.get('user_id', ''),
                    str(event.get('metadata', {}))
                ])
        except Exception as e:
            # Don't fail if CSV write fails
            print(f"Warning: Failed to write telemetry to CSV: {e}")


def get_metrics() -> dict:
    """
    Get current metrics summary
    
    Returns:
        Dictionary containing:
        - counters: All counter values
        - recent_events: Last 10 events
        - total_events: Total event count
    """
    with _lock:
        return {
            "counters": dict(_counters),
            "recent_events": _events[-10:] if _events else [],
            "total_events": len(_events),
            "csv_path": str(TELEMETRY_FILE.absolute())
        }


def increment_counter(key: str, value: int = 1) -> None:
    """
    Manually increment a counter
    
    Args:
        key: Counter key
        value: Increment value (default: 1)
    """
    with _lock:
        _counters[key] += value


def get_counter(key: str) -> int:
    """
    Get counter value
    
    Args:
        key: Counter key
        
    Returns:
        Counter value (0 if not found)
    """
    with _lock:
        return _counters.get(key, 0)


def reset_metrics() -> None:
    """
    Reset all in-memory metrics (for testing)
    CSV file is not affected
    """
    global _events, _counters
    with _lock:
        _events.clear()
        _counters.clear()



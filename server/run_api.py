#!/usr/bin/env python3
"""Run the GDPR Anonymizer API server."""

import logging.config
import logging
import uvicorn
import yaml

with open('logging.yaml', 'r') as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)
    
if __name__ == "__main__":
    # Load your config first

    # Start uvicorn with log_config=None to prevent it from overriding
    uvicorn.run(
        "anonymization.interfaces.rest.main:app",
        host="0.0.0.0",
        port=8000,
        log_config=None,  # ← Important!
        reload=True
    )

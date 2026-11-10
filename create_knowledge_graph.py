#!/usr/bin/env python3
"""
synthetic-ppi - BioCypher project for the Synthetic Protein Interaction Dataset

This script creates a knowledge graph using BioCypher and the SyntheticPpiAdapter.
"""

import logging
import os
from pathlib import Path

from biocypher import BioCypher
from synthetic_ppi.adapters.synthetic_ppi_adapter import SyntheticPpiAdapter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to create the knowledge graph."""
    logger.info("Starting synthetic-ppi knowledge graph creation")
    
    # Initialize BioCypher
    bc = BioCypher(
        biocypher_config_path=os.environ.get("BIOCYPHER_CONFIG_PATH", "config/biocypher_config.yaml"),
        schema_config_path="config/schema_config.yaml"
    )
    
    # Initialize the adapter
    # TODO: Configure your data source here. The adapter ignores it
    # and yields dummy data until get_nodes() and get_edges() are implemented.
    data_source = "data/your_data"  # Update this with your actual data source
    
    adapter = SyntheticPpiAdapter(
        data_source=data_source,
        # Add any additional configuration parameters here
    )
    
    # Create the knowledge graph
    logger.info("Creating knowledge graph...")
    bc.write_nodes(adapter.get_nodes())
    bc.write_edges(adapter.get_edges())
    
    logger.info("Knowledge graph creation completed successfully!")

    # Offline mode: write the Neo4j import script and create final summary
    try:
        import_call = bc.write_import_call()
    except NotImplementedError:
        logger.info("Online mode: data was written directly to Neo4j")
    else:
        logger.info(f"Import script written to {import_call}")
        bc.summary()


if __name__ == "__main__":
    main()

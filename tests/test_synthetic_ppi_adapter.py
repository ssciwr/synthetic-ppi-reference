"""
Tests for SyntheticPpiAdapter.
"""

import pytest
from pathlib import Path
import tempfile
import pandas as pd

from synthetic_ppi.adapters.synthetic_ppi_adapter import SyntheticPpiAdapter


class TestSyntheticPpiAdapter:
    """Test the SyntheticPpiAdapter."""
    
    def test_adapter_initialization(self):
        """Test that the adapter initializes correctly."""
        adapter = SyntheticPpiAdapter("test_data_source.csv")
        
        assert adapter.data_source == "test_data_source.csv"
        assert adapter.config == {}
    
    def test_adapter_initialization_with_config(self):
        """Test that the adapter initializes with additional config."""
        config = {"param1": "value1", "param2": "value2"}
        adapter = SyntheticPpiAdapter("test_data_source.csv", **config)
        
        assert adapter.data_source == "test_data_source.csv"
        assert adapter.config == config
    
    def test_get_metadata(self):
        """Test that metadata is returned correctly."""
        adapter = SyntheticPpiAdapter("test_data_source.csv")
        metadata = adapter.get_metadata()
        
        assert metadata["name"] == "SyntheticPpiAdapter"
        assert metadata["data_source"] == "test_data_source.csv"
        assert metadata["data_type"] == "file"
        assert metadata["version"] == "0.1.0"
        assert metadata["adapter_class"] == "SyntheticPpiAdapter"
    
    def test_get_nodes(self):
        """Test that nodes are returned."""
        adapter = SyntheticPpiAdapter("test_data_source.csv")
        nodes = list(adapter.get_nodes())
        
        # Adapter now returns dummy data, not data from the data source
        # Check that nodes are tuples with 3 elements (node_id, node_label, properties_dict)
        assert len(nodes) > 0
        assert isinstance(nodes[0], tuple)
        assert len(nodes[0]) == 3
        node_id, node_label, properties = nodes[0]
        assert isinstance(node_id, str)
        assert isinstance(node_label, str)
        assert isinstance(properties, dict)
    
    def test_warns_about_dummy_data(self, caplog):
        """Test that the unimplemented adapter warns that it yields dummy data."""
        SyntheticPpiAdapter("test_data_source.csv")
        
        assert "dummy data" in caplog.text
    
    def test_validate_data_source_with_existing_csv(self):
        """Test data source validation with existing CSV file."""
        # Create a temporary CSV file
        test_data = pd.DataFrame({'id': ['1'], 'name': ['test']})
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            test_data.to_csv(f, index=False)
            temp_file = f.name
        
        try:
            adapter = SyntheticPpiAdapter(temp_file)
            assert adapter.validate_data_source() is True
        finally:
            Path(temp_file).unlink()
    
    def test_validate_data_source_with_nonexistent_file(self):
        """Test data source validation with non-existent file."""
        adapter = SyntheticPpiAdapter("nonexistent_file.csv")
        assert adapter.validate_data_source() is False
    
    def test_get_edges_empty(self):
        """Test that edges are returned."""
        adapter = SyntheticPpiAdapter("test_data_source.csv")
        edges = list(adapter.get_edges())
        
        # Adapter now returns dummy edges
        # Check that edges are tuples with 5 elements (edge_id, source_id, target_id, edge_label, properties_dict)
        assert isinstance(edges, list)
        assert len(edges) > 0
        assert isinstance(edges[0], tuple)
        assert len(edges[0]) == 5
        edge_id, source_id, target_id, edge_label, properties = edges[0]
        assert edge_id is None or isinstance(edge_id, str)
        assert isinstance(source_id, str)
        assert isinstance(target_id, str)
        assert isinstance(edge_label, str)
        assert isinstance(properties, dict)

    def test_edge_endpoints_match_schema_node_types(self):
        """Test that edge sources and targets are nodes of the schema's types."""
        adapter = SyntheticPpiAdapter("test_data_source.csv")
        node_types = {node_id: node_label for node_id, node_label, _ in adapter.get_nodes()}

        # protein_encoded_by_gene in schema_config.yaml: source protein, target gene
        for _, source_id, target_id, _, _ in adapter.get_edges():
            assert node_types.get(source_id) == "protein"
            assert node_types.get(target_id) == "gene"

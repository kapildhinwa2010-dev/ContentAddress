import pytest
import torch
from contentaddress import ContentAddress, create_contentaddress

class TestContentAddress:
    def test_init(self):
        m = ContentAddress(dim=256, hidden_dim=512)
        assert m.dim == 256
    
    def test_forward(self):
        m = ContentAddress(dim=256)
        x = torch.randn(32, 256)
        assert m(x).shape == (32, 256)
    
    def test_factory(self):
        m = create_contentaddress()
        assert isinstance(m, ContentAddress)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

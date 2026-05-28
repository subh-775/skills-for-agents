"""
Fix Triton 3.7 + PyTorch 2.6 incompatibility.
Must be imported BEFORE torch.compile is used.
"""

class AttrsDescriptor(dict):
    """Shim for old Triton AttrsDescriptor API. Inherits dict for Triton 3.7 compat."""
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.property_values = {"tt.divisibility": 16, "tt.equal_to": 1}
        self.equal_to_1 = []
        self.divisible_by_16 = []
    @classmethod
    def from_dict(cls, d):
        arg_props = d.get('arg_properties', {})
        obj = cls(**arg_props)
        return obj
    def __repr__(self):
        return f"AttrsDescriptor(divisible_by_16={self.divisible_by_16}, equal_to_1={self.equal_to_1})"

import triton.backends.compiler as _bc
_bc.AttrsDescriptor = AttrsDescriptor

import triton.compiler.compiler as _cc
_cc.AttrsDescriptor = AttrsDescriptor

if not hasattr(_cc, 'triton_key'):
    def _triton_key():
        import hashlib
        return hashlib.sha256(b"triton-3.7-shim").hexdigest()
    _cc.triton_key = _triton_key

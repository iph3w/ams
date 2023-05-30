from .discovery import (
    ListView as DiscoveryListView,
    CreateView as DiscoveryCreateView,
    DetailView as DiscoveryDetailView
)

from .scanner import (
    ListView as ScannerListView,
    CreateView as ScannerCreateView,
    DetailView as ScannerDetailView
)

__all__ = [
    'DiscoveryListView', 'DiscoveryCreateView', 'DiscoveryDetailView',
    'ScannerListView', 'ScannerCreateView', 'ScannerDetailView'
]

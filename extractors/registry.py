from typing import Type, Optional, Dict, List

from extractors.base import DimensionExtractor


class ExtractorRegistry:
    """Registry for dimension extractors using decorator pattern."""
    
    _extractors: Dict[str, Type[DimensionExtractor]] = {}
    
    @classmethod
    def register(cls, name: str):
        """Decorator to register an extractor class."""
        def decorator(extractor_class: Type[DimensionExtractor]):
            cls._extractors[name] = extractor_class
            return extractor_class
        return decorator
    
    @classmethod
    def get(cls, name: str) -> Optional[Type[DimensionExtractor]]:
        """Get an extractor class by name."""
        return cls._extractors.get(name)
    
    @classmethod
    def create(cls, name: str, **kwargs) -> DimensionExtractor:
        """Create an extractor instance by name."""
        extractor_class = cls._extractors.get(name)
        if not extractor_class:
            raise ValueError(f"Unknown extractor: {name}")
        return extractor_class(**kwargs)
    
    @classmethod
    def available(cls) -> List[str]:
        """Return list of available extractor names."""
        return list(cls._extractors.keys())

import uuid
import datetime
from deepdue.enums import CacheEntityType
from qdrant_client import QdrantClient, models

class QdrantCHCache:
    def __init__(self, qdrant_host: str, qdrant_port: str, cache_ttl_seconds: int) -> dict | None:
        self.cache_ttl_seconds = cache_ttl_seconds
        self.client = QdrantClient(url=qdrant_host, port=qdrant_port)
        self._initialize_collections()

    def _collection_name(self, entity_type: CacheEntityType) -> str: 
        return f"ch_{entity_type.value}"
    
    def _initialize_collections(self):
        existing = [c.name for c in self.client.get_collections().collections]
        for name in [self._collection_name(cache_name) for cache_name in CacheEntityType]:
            if name not in existing:
                self.client.create_collection(
                    collection_name=name,
                    vectors_config=models.VectorParams(size=1, distance=models.Distance.COSINE)
                )
    
    def get(self, entity_id: str, entity_type: CacheEntityType):
        results = self.client.scroll(
            collection_name=self._collection_name(entity_type),
            scroll_filter=models.Filter(
                must=[models.FieldCondition(
                    key="entity_id", 
                    match=models.MatchValue(value=entity_id)
                    )]
            ),
            limit=1,
            with_payload=True
        )

        points, _ = results
        if not points:
            return None
        
        cached_at = datetime.datetime.fromisoformat(points[0].payload["cached_at"])
        age = (datetime.datetime.now(datetime.timezone.utc) - cached_at).total_seconds()
        
        if age > self.cache_ttl_seconds:
            return None
        
        return points[0].payload["data"]
    
    def set(self, entity_id: str, entity_type: CacheEntityType, data: dict) -> None:
        self.client.upsert(
            collection_name=self._collection_name(entity_type),
            points=[models.PointStruct(
                id=str(uuid.uuid4()),
                vector=[0.0],
                payload={
                    "entity_id": entity_id,
                    "cached_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "data": data
                }
            )]
        )

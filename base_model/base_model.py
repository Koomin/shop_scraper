from elasticsearch_dsl import (Document, Date, Text, Integer, Float, Keyword, Index, Search)


class BaseModel(Document):
    manufacturer_id = Keyword()
    manufacturer = Keyword()
    model = Keyword()
    price = Float()
    add_date = Date()

    def save(self, **kwargs):
        self.meta.id = self.manufacturer_id
        super().save(**kwargs)

class MediaRouter:
    def db_for_read(self, model, **hints):
        if model.__name__ == 'Movie':
            return 'movies_db'
        elif model.__name__ == 'Drama':
            return 'dramas_db'
        elif model.__name__ == 'Singer':
            return 'singers_db'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        # 다른 DB간 관계 허용 안 함
        return False
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name is None:
            return None
        model_name = model_name.lower()
        if model_name == 'movie':
            return db == 'movies_db'
        elif model_name == 'drama':
            return db == 'dramas_db'
        elif model_name == 'singer':
            return db == 'singers_db'
        return None

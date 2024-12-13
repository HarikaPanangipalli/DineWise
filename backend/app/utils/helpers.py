from bson import ObjectId
from fastapi.encoders import jsonable_encoder

<<<<<<< HEAD

=======
>>>>>>> main
class JSONEncoder:
    @staticmethod
    def encode(obj):
        def convert(o):
            if isinstance(o, ObjectId):
                return str(o)
            return jsonable_encoder(o)
<<<<<<< HEAD

        return convert(obj)
=======
        return convert(obj)
>>>>>>> main

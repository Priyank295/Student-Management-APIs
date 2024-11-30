from motor.motor_asyncio import AsyncIOMotorClient

# Connect to MongoDB Atlas
MONGO_URL = "mongodb+srv://vp2952004:dafar2952004@mycluster.penf2wk.mongodb.net/student_management?retryWrites=true"
client = AsyncIOMotorClient(MONGO_URL)
database = client.student_management
students_collection = database.get_collection("students")


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "address": student["address"]
    }
    
def student_helper_id(student) -> dict:
    return {
        "name": student["name"],
        "age": student["age"],
        "address": {
            "city": student["address"]["city"],
            "country": student["address"]["country"]
        }
    }

def student_name_age(student) -> dict:
    return {
        "name": student["name"],
        "age": student["age"],
    }

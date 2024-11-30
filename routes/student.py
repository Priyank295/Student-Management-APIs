from fastapi import APIRouter, HTTPException, Query, Path, Body
from models.student import Student
from typing import List, Optional
from services.database import students_collection, student_helper, student_helper_id, student_name_age
from bson import ObjectId

router = APIRouter()

@router.post("/", status_code=201)
async def create_student(student: Student):
   
    student_data = student.dict()
    result = await students_collection.insert_one(student_data)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create student")


    return {"id": str(result.inserted_id)}

@router.get("/", status_code=200)
async def list_students(
    country: Optional[str] = Query(None, description="Filter by country"),
    age: Optional[int] = Query(None, description="Filter by minimum age")
):

    query = {}

   
    if country:
        query["address.country"] = country

    
    if age is not None:
        query["age"] = {"$gte": age}

    
    students_cursor = students_collection.find(query)
    students = [student_name_age(student) for student in await students_cursor.to_list(length=100)]

    return {"data": students}



@router.get("/{id}", status_code=200)
async def fetch_student(
    id: str = Path(..., description="The ID of the student previously created.")
):

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

   
    student = await students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    
    return student_helper_id(student)


@router.patch("/{id}", status_code=204)
async def update_student(
    id: str = Path(..., description="The ID of the student to update."),
    student_update: dict = Body(
        ...,
        description="Properties to update for the student.",
        example={
            "name": "Jane Doe",
            "age": 22,
            "address": {"city": "Los Angeles", "country": "USA"},
        },
    ),
):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    
    update_query = {}
    if "name" in student_update:
        update_query["name"] = student_update["name"]
    if "age" in student_update:
        update_query["age"] = student_update["age"]
    if "address" in student_update:
        update_query["address"] = {
            "city": student_update["address"].get("city"),
            "country": student_update["address"].get("country"),
        }

   
    if not update_query:
        raise HTTPException(status_code=400, detail="No valid fields to update")

   
    result = await students_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": update_query}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    
    return {}



@router.delete("/{id}", status_code=200)
async def delete_student(
    id: str = Path(..., description="The ID of the student to delete.")
):
   
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

   
    result = await students_collection.delete_one({"_id": ObjectId(id)})

    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")


    return {}
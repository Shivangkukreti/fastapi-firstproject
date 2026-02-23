from fastapi import FastAPI,File, Form,UploadFile,HTTPException,Depends
from db.data_base import fruits_collection,students_collection,user_collection
from util.auth import create_access_token,get_password_hash,verify_password,get_current_user
from bson import ObjectId
from db.db_model import Fruit,Student,pfp,User,Userlogin,Token,userout
from util.image import imagekit
app = FastAPI()

@app.get("/x")
def any():
    return {"message": "Hello World"}


fruits={1: {"name": "Apple", "price": 1.2, "quantity": 10},
        2: {"name": "Banana", "price": 0.8, "quantity": 20},
        3: {"name": "Orange", "price": 1.5, "quantity": 15},
        4: {"name": "Grapes", "price": 2.0, "quantity": 8},}


@app.get("/fruits")
def get_fruits(limit: int = None):
    if limit is None:
        return list(fruits.values())
    return list(fruits.values())[:limit]


@app.post('/add-fruit')
async def add_fruits(data: Fruit):
    try:
        x = data.model_dump()
        result = await fruits_collection.insert_one(x)
        return {
            "message": "Fruit added successfully",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        return {"REAL_ERROR": str(e)}
    


@app.get('/get-fruits')
async def get_fruits():
    try:
        fruits = []
        cursor = fruits_collection.find({})
        async for document in cursor:
            document['_id'] = str(document['_id'])
            fruits.append(document)
        return fruits
    except Exception as e:
        return {"REAL_ERROR": str(e)}
    

@app.get('/get-fruit/{fruit_id}')
async def get_that_fruit(fruit_id:str):
    try:
        fruit=await fruits_collection.find_one({"_id":ObjectId(fruit_id)})
        if fruit:
            fruit['_id']=str(fruit['_id'])
            return {"message":"Fruit found","fruit":fruit}
        else:
            return {"message":"Fruit not found"}
    except Exception as e:
        return {"REAL_ERROR": str(e)}
    

@app.post('/delete-fruit/{fruit_id}')
async def del_fruit(fruit_id:str):
    
       x = await fruits_collection.delete_one({"_id":ObjectId(fruit_id)})
       if x.deleted_count == 0:
           return {"message":"Fruit not found"}
       else:
           return {"message":"Fruit deleted successfully","data":x.deleted_count}
       

# ---------------------------------------------------------------------------

@app.post('/add-student')
async def add_student(data:Student):
    try:
        x=data.model_dump()
        result=await students_collection.insert_one(x)
        return {    "message":"Student added successfully",
                    "id":str(result.inserted_id)}
    except Exception as e:
        return {"REAL_ERROR":str(e)}
    

@app.get('/get-students')
async def get_students():
    try:
        students=[]
        all=await students_collection.find({}).to_list(length=None)
        print(all)
        for student in all:
            student['_id']=str(student['_id'])
            students.append(student)
            print(len(students))
        return students
    except Exception as e:
        return {"REAL_ERROR": str(e)}
    

@app.get('/get-student/{id}')
async def get_student(id:str):
    try:
        if not id:
            return {"message":"ID is required"}
        stu=await students_collection.find_one({"_id":ObjectId(id)})
        if not stu:
            return {"message":"Student not found"}
        stu['_id']=str(stu['_id'])
        return {"message":"Student found","student":stu}
    except Exception as e:
        return {"REAL_ERROR": str(e)}
    


@app.post('/up-img')
async def up_img(name: str=Form(...), img: UploadFile = File(...)):
    try:
        content=await img.read()
        response=imagekit.files.upload(file=content,file_name=img.filename,folder="pfp")
        await students_collection.insert_one({"name":name,"photo":response.url})
        return {"message":"Image uploaded successfully"}
    except Exception as e:
        return {"REAL_ERROR": str(e)}
    

@app.post('/up-img2',response_model=pfp)
async def up(name:str=Form(...),img:UploadFile=File(...)):
    try:
        content=await img.read()
        response=imagekit.files.upload(file=content,file_name=img.filename,folder="pfp")
        x=pfp(photo=response.url,name=name)
        await students_collection.insert_one(x.model_dump())
        return x
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    

# ----------------------------------------------------------------------------



@app.post('/signup',response_model=Token)
async def signup(data:User):
    try:
        existing_user=await user_collection.find_one({"email":data.email})
        if existing_user:
           raise HTTPException(status_code=400,detail="Email already registered")
        hashed_pass=get_password_hash(data.password)
        any=data.model_dump()
        any['password']=hashed_pass
        await user_collection.insert_one(any)
        token=create_access_token({"email":any['email']})
        return {"message":"User created successfully","token":token}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@app.post('/login',response_model=Token)
async def login(data:Userlogin):
    try:
        user=await user_collection.find_one({"email":data.email})
        if not user:
            raise HTTPException(status_code=401,detail="Invalid credentials")
        if not verify_password(data.password,user['password']):
            raise HTTPException(status_code=401,detail="Invalid credentials")
        token=create_access_token({"email":user['email']})
        return {"access_token":token,"message":"user logged in successfully"}
    except Exception as e:
       raise HTTPException(status_code=500,detail=str(e))
    

@app.get('/me',response_model=userout)
async def me(current_user: dict = Depends(get_current_user)):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    


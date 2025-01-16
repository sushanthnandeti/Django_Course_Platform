import cloudinary
from decouple import config # os.environ.get()

CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default = "")
CLOUDINARY_PUBLIC_API_KEY = config("CLOUDINARY_PUBLIC_API_KEY", default = "874837483274837")
CLOUINARY_SECRET_API_KEY = config("CLOUINARY_SECRET_API_KEY")

def cloudinary_init():
    cloudinary.config( 
        cloud_name = "courses", 
        api_key = "874837483274837", 
        api_secret = "a676b67565c6767a6767d6767f676fe1",
        secure = True
)
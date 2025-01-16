import cloudinary
from decouple import config # os.environ.get()

CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default = "")
CLOUDINARY_PUBLIC_API_KEY = config("CLOUDINARY_PUBLIC_API_KEY", default = "391824773992115")
CLOUINARY_SECRET_API_KEY = config("CLOUINARY_SECRET_API_KEY")

def cloudinary_init():
    cloudinary.config( 
        cloud_name = "dt3xitblp", 
        api_key = "391824773992115", 
        api_secret = "-Ey03hpKSrKtyWeHy7MTHtHGliY",
        secure = True
)
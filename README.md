## API Spec

### /api/user/signup/ 
**Method** = POST  
*Body*:  
```json
{
	"email": String,
	"password": String,
	"username": String
}  
*Response*
```json
{
    "data": {
        "id": Int,
        "email": String,
        "username": String,
        "profilePictureURL": String,
        "posts": Array<Post>
    },
    "accessToken": String
}
		
```




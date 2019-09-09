## AWS Architecture
<img src="https://github.com/seancorc/Hanger-Backend/blob/master/AWSDiagram.png" width="450">

## API Spec

### User:

#### POST /api/user/signup/   
*Body*:  
```json
{
	"email": "String",
	"password": "String",
	"username": "String"
} 
```
*Successful Response (201)*:
```json
{
    "data": {
        "id": "Int",
        "email": "String",
        "username": "String",
        "profilePictureURL": "String or None",
        "posts": "Array<Post>"
    },
    "accessToken": "String"
}	
```

#### POST /api/user/login/   
*Body*:  
```json
{
	"email": "String",
	"password": "String",
} 
```
*Successful Response (200)*:
```json
{
    "data": {
        "id": "Int",
        "email": "String",
        "username": "String",
        "profilePictureURL": "String or None",
        "posts": "Array<Post>"
    },
    "accessToken": "String"
}	
```

#### PUT /api/user/updateinfo/   
*Headers*: 
```json
{
	"Authorization": "Bearer accessToken"
}
```
*Body*:  
```json
{
	"newEmail": "String",
	"newUsername": "String"
} 
```
*Successful Response (200)*:
```json
{
    "data": {
        "id": "Int",
        "email": "String",
        "username": "String",
        "profilePictureURL": "String or None",
        "posts": "Array<Post>"
    }
}	
```


#### PUT /api/user/updatepassword/   
*Headers*: 
```json
{
	"Authorization": "Bearer accessToken"
}
```
*Body*:  
```json
{
	"currentPassword": "String",
	"newPassword": "String"
} 
```
*Successful Response (200)*:
```json
{
    "success": "True"
}	
```

#### PUT /api/user/profilepicture/   
*Headers*: 
```json
{
	"Authorization": "Bearer accessToken"
}
```
*Body*:  
```json
{
	"url": "String"
} 
```
*Successful Response (200)*:
```json
{
    "success": "True"
}	
```

#### PUT /api/user/location/   
*Headers*: 
```json
{
	"Authorization": "Bearer accessToken"
}
```
*Body*:  
```json
{
	"lat": "Float",
	"longt": "Float"
} 
```
*Successful Response (200)*:
```json
{
        "data": {
        "id": "Int",
        "email": "String",
        "username": "String",
        "profilePictureURL": "String or None",
        "posts": "Array<Post>"
    }
}	
```

### Selling and Buying Clothes

#### POST /api/post/create/   
*Headers*: 
```json
{
	"Authorization": "Bearer accessToken"
}
```
*Body*:  
```json
{
	"clothingType": "String",
	"category": "String",
	"name": "String",
	"brand": "String",
	"price": "String",
	"description": "String or None",
	"imageURLs": "[String]"
}
```
*Successful Response (201)*:
```json
{
    "data": {
        "id": "Int",
 		"clothingType":"String",
		"category":" String",
		"name":" String",
		"brand": "String",
		"price": "String",
		"description": "String or None",
        "user": {
            "id": "Int",
            "email": "String",
            "username": "String",
            "profilePictureURL": "String or None"
        },
		"imageURLs": "[String]"
    }
}	
```

#### GET /api/user/posts/{optional URL Parameters: 'minPrice', 'maxPrice', 'radius', 'types, 'categories'}
*Headers*: 
```json
{
	"Authorization": "Bearer accessToken"
}
```
*Successful Response (201)*:  
```json
{
    "data": [
    {
        "id": "Int",
 		"clothingType":"String",
		"category":" String",
		"name":" String",
		"brand": "String",
		"price": "String",
		"description": "String or None",
		"imageURLs": "[String]"
     },
     {
     	"id": "Int",
 		"clothingType":"String",
		"category":" String",
		"name":" String",
		"brand": "String",
		"price": "String",
		"description": "String or None",
		"imageURLs": "[String]"
     }
    ]
}
```

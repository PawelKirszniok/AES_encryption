# Books_API


## Table of contents

* .[About](#about)
* .[Requirements](#requirements)
* .[API Documentation](#documentation)


## About

a simple API in Fast API implementing AES 128 for characters available via the python chr and ord functions. 


## Requirements: 

The stated requirements were to implement a cypher and expose its encode and decode methods via FastAPI behind a Basic Auth authentication. 

Minimum requirements were handling latin uppercase and lowercase letters, numbers and several whitespace characters.


## Documentation:

The API exposes two endpoints:

both of them require the request body schema below: 

~~~
{
	"key": "string" # not less than 16 characters
	"text" : "string" # plaintext for the encode method and cyphertext for the decode method 

}
~~~

in addition to that you need to satisfy the requirements for Basic Auth by providing valid a username and password in the header of your request.

#### /encode

request type : POST 

This endpoint treats the text field as plaintext and returns an encrypted version of it. The string length will be rounded up to the neearest 16 character multiple

#### /decode 

request type : POST

This endpoint treats the text field as cyphertext and returns the unencrypted string.



Documentation available also online when hosted in the  '/docs#/' path


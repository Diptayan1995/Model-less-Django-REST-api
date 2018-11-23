

###Django Rest Framework witout default model and serializers module###



Django is an extremely popular server-side web framework, written in Python because of its “batteries included” philosophy(Object  relational mapping, model view controller based design, multi-lingual support, package management etc), immense scalability, security modules, stellar documentation, huge community and many more reasons. But the components in Django are too tightly coupled and everything depends on the ORM, thus making this framework too monolithic.
	 So in some cases it’s more flexible to replace ORM-driven code by raw SQL code or SQLAlchemy and implement your own authentication measures in stead of using default django auth modules.
This repository contains a REST api built with django-rest-framework without the default model and seralizer module. A simple login,registration service is built over it and the user authentication is done using JWT.


Steps:
##1. Remove this import module statements in settings.py.



['django.contrib.auth.middleware.AuthenticationMiddleware', 
'django.contrib.auth.middleware.SessionAuthenticationMiddleware'] in MIDDLEWARE = []




'django.contrib.auth.context_processors.auth' in TEMPLATES = {'OPTIONS':}





Remove AUTH_PASSWORD_VALIDATORS  import module.

 AUTH_PASSWORD_VALIDATORS = [
					    {
						'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
					    },
					    {
						'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
					    },
					    {
						'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
					    },
					    {
						'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',}]








##2. Add an 'EXCEPTION_HANDLER’ module in REST_FRAMEWORK = [].

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'UNAUTHENTICATED_USER': None
}






##3.  Create model fields in  __init__.py and import the model in seralizers.py
(this step is optional)

 




##4. To remove the the default serializer module dependency serialize the json data for viewset without serialzers module.
Viewsets in django rest framework takes OrderedDict() for get request and json data for post put and delete request.  After reformatting(serializing) the data format for viewsets the model imports from __init__.py and the default serializers import from serializers.py can be removed from view.py.



Now you can create, import and query your own data model from the database you choose(I have used postgres here) by raw SQL coding. Moreover, you can choose your own user authentication and session management mechanism. Here , I am using JWT and sending it to the API in request body. But the better approach is to send the JWT in the Authorization header of the request. Hence the data models and the user authentication do not depend on the django ORM any more.

 




 
   


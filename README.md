# CL_MarketPlace
<b>CL Market is an achivement of E-commerce website which allow user to create an account and buy/sell their products or skills just similar to <a href="www.udemy.com">Udemy</a></b>
<br><br>
The project including the features and requirements below:<br>
* Front-End: HTML, CSS, JavaScript(pagination, sliding image and else...), JQuery<br>
* Back-End: Python, Django<br>
* Third-Party APIs: Facebook login, BrainTree payment, Twilio SMS, Zendesk online chatting<br>
* Deployment: Heroku web service, Amazon S3 storage, Dj-database-url<br>

***
Most of the ideas are clean and easy to understand if you read my souce code, the only thing I would like to memtion is the potential problem you might meet during deployment.

I personaly prefer Heroku web service for deployment my project on internet, Heroku is a git base system. It's super easy to build the environment for you base on the requirement.txt file. But there are some limitations when you use Heroku:

1. Heroku natively uses postgres. Life will be easier for you if you use that locally. But you can still use other db system and convert it to postgres by some tools, check dj-database-url for django project.
2. Heroku doesn't guarantee to store your static files permanently (especially for user upload image files !). I highly suggest to use Amazon S3 to store your static files and just set up the correct token and path for Heroku. 

In this project, I'm using Amazon S3 to store media file. You can check my settings.py to get the idea how to set up the credential required by Amazon S3. You will also need to setup the corresponding info as variables on your Heroku repo. Also change your template for the url link. 

To check the result of this project: 
click here: <a href="https://serene-fjord-52474.herokuapp.com/">CL MarketPlace</a>

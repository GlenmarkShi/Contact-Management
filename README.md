# Contact-Management
Contact Management using Laravel API for uploading and managing contacts and a Python service for processing and storing contact data in MongoDB database

step 1: clone the project 
git clone https://github.com/GlenmarkShi/Contact-Management.git

step 2: navigate to api folder
cd api

step 3: install dependencies listed in composer.json
composer install

step 3: navigate to your api folder and copy the .env.example and paste it to api folder
step 4: after copying rename the duplicate to .env

step 5: configure the environment for monggo db
DB_CONNECTION=mongodb
DB_HOST=127.0.0.1
DB_PORT= YOUR PORT NUMBER
DB_DATABASE= YOUR DATABASE NAME
DB_USERNAME= YOUR DATABASE USERNAME
DB_PASSWORD= YOUR DATABASE PASSWORD

step 6: generate your application key
php artisan key:generate

step 7: run migration
php artisan migrate

step 8: php artisan serve
